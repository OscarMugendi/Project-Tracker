import { Injectable } from '@angular/core';
import { HttpClient, HttpInterceptor,HttpRequest,HttpHandler,HttpEvent, HttpHeaders, HttpResponse } from '@angular/common/http';
import { CanActivate, Router } from '@angular/router';

import { Observable } from 'rxjs';
import { tap, shareReplay, map } from 'rxjs/operators';
import 'rxjs/add/operator/map';

import * as jwtDecode from 'jwt-decode';
import * as moment from 'moment';

import { environment } from 'src/environments/environment';

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json'
  })
};

@Injectable({
  providedIn: 'root'
})

export class AuthService {

  private apiRoot = 'http://127.0.0.1:8000/auth/register/';

  constructor(private http: HttpClient) { }

  // private setSession(authResult:any){
  //   const token = authResult.token;
  //   const payload = <JWTPayload> jwtDecode(token);
  //   const expiresAt = moment.unix(payload.exp);
  // }
  // localStorage.setItem('token',authResult.token);
  // localStorage.setItem('expires_at',JSON.stringify(expiresAt.valueOf()));

}
