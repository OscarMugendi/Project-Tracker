import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { FormsModule } from "@angular/forms";
import { Observable } from "rxjs";

@Injectable({
    providedIn: 'root'
})

export class ProjectService{
    api_link: string = "http://localhost:8000/";
    constructor( private http: HttpClient) { }

    getprojects(){
        return this.http.get(this.api_link + 'auth/api/projects/');
    }

}