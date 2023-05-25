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

  constructor(private service: VideoConnectService, private socket: Socket) { } 
  
  ngOnInit(): void {
    // this.startstream();
    this.videoElement.nativeElement.style.display = 'block';
  }

  startStream(): void {
    this.videoElement.nativeElement.style.display = 'block';
    this.capturing = true;
    navigator.mediaDevices.getUserMedia({ video: true })
      .then((stream: MediaStream) => {
        this.videoStream = stream;
        this.videoElement.nativeElement.srcObject = stream;
        this.capturing = true;
        this.frameInterval = setInterval(() => this.streamFrame(), 1000 / 1000);
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