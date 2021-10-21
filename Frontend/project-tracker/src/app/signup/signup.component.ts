import { Component, OnInit } from '@angular/core';
import { FormBuilder,FormGroup } from '@angular/forms';

import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';


@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {
  register: any;

  signupForm: FormGroup;

  constructor(
    public fb: FormBuilder,
    public authService: AuthService,
    public router: Router
  ) { 
    this.signupForm = this.fb.group({
      name: [''],
      email: [''],
      password: ['']
    })
  }

  ngOnInit(): void {
    this.register = {
      username: '',
      email: '',
      password: '',
    }
  }

  registerUser(){
    
    this.authService.signUp(this.register).subscribe((res)=>{
      if (res.result){
        this.signupForm.reset()
      }
      this.router.navigate(['login']);
    })
  }

}
