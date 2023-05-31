import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { VideoConnectService } from 'src/app/_services/video-connect.service';
import { Socket } from 'ngx-socket-io';

@Component({
  selector: 'app-video-stream',
  templateUrl: './video-stream.component.html',
  styleUrls: ['./video-stream.component.css']
})
export class VideoStreamComponent implements OnInit {
  @ViewChild('videoElement', { static: true }) videoElement: ElementRef;
  videoStream: MediaStream;
  capturing: boolean = false;
  frameInterval: any;
  idea: string = "hey";
  videoFlask: string;
  selectedCamera: string;
  cameras: MediaDeviceInfo[];

  constructor(private service: VideoConnectService, private socket: Socket) { } 
  
  ngOnInit(): void {
    // this.startstream();
    this.enumerateDevices();
    this.videoElement.nativeElement.style.display = 'block';
  }

  enumerateDevices(): void {
    navigator.mediaDevices.enumerateDevices()
      .then((devices: MediaDeviceInfo[]) => {
        this.cameras = devices.filter(device => device.kind === 'videoinput');
        if (this.cameras.length > 0) {
          this.selectedCamera = this.cameras[0].deviceId;
        }
      })
      .catch((error: any) => {
        console.error('Error enumerating devices:', error);
      });
  }

  changeCamera(): void {
    this.stopStream();
    this.startStream();
  }

  startStream(): void {
    this.videoElement.nativeElement.style.display = 'block';
    this.capturing = true;
    navigator.mediaDevices.getUserMedia({ video: {
      deviceId: this.selectedCamera ? { exact: this.selectedCamera } : undefined
        } 
      }).then((stream: MediaStream) => {
        this.videoStream = stream;
        this.videoElement.nativeElement.srcObject = stream;
        this.capturing = true;
        this.frameInterval = setInterval(() => this.streamFrame(), 500);
      })
      .catch((error) => {
        console.error('Error accessing video stream:', error);
      });
    // this.socket.on('video_stream', (base64Image: string) => {
    //   this.videoFlask = 'data:image/jpeg;base64,' + base64Image;
    //   });
  }

  stopStream(): void {
    // this.videoElement.nativeElement.style.display = 'none';
    this.capturing = false;
    if (this.frameInterval) {
      clearInterval(this.frameInterval);
      this.videoFlask = 'block';
    }
    if (this.videoStream) {
      this.videoStream.getTracks().forEach(track => track.stop());
    }
  }

  streamFrame(): void {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    const video = this.videoElement.nativeElement;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL('image/jpeg');
    this.postDataFunction(imageData);
  }

  postDataFunction(imageData: String): void{
    this.service.postDataToFlask(imageData).subscribe( 
      (response) => {
        this.idea = JSON.parse(response);
        this.videoFlask = this.idea["message"];
      },
      (error) => {
        console.error('Error sending frame to Flask:', error);
      }
    );
  }
}