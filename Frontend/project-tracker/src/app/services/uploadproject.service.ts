import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})


export class UploadprojectService {
  api_link: string = "http://localhost:8000/";

  constructor(private http: HttpClient) { }

  uploadProject(data:any){
    return this.http.post(this.api_link + 'auth/api/projects/new', data);
  }
  
}
