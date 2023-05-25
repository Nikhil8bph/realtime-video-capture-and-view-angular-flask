import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class VideoConnectService {

  constructor(private http: HttpClient) { }

  private FLASK_URL = environment.backend;

  postDataToFlask(imageData: String) {
    return this.http.post(this.FLASK_URL+"process_frame",imageData,{ responseType: 'text' });
  }
}
