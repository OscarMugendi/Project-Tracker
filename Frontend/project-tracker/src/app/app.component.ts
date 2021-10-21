import { Component, OnInit } from '@angular/core';
import { ProjectService } from './services/project.service';
import { AuthService } from './_services/auth.service';
import { UserService } from './services/user.service';
import { throwError } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'project-tracker';
  public user: any;

  constructor(public authService: AuthService){

  }
  ngOnInit(){
    this.user = {
      username: '',
      password: '',

    };
  }
  // logout(){
  //   this.authService.doLogout()
  // }
}


