import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ProjectService } from './services/project.service';
import { UserService } from './services/user.service';
import { AppComponent } from './app.component';
import { NavbarComponent } from './navbar/navbar.component';
import { AppRoutingModule } from './app-routing.module'; 
import { HomeComponent } from './home/home.component';
import { ProjectPageComponent } from './project-page/project-page.component';
import { SignupComponent } from './signup/signup.component';
import { LoginComponent } from './login/login.component';
import { StudentProfileComponent } from './student-profile/student-profile.component';
import { ProfileComponent } from './profile/profile.component';

import { HttpClientModule,HTTP_INTERCEPTORS } from '@angular/common/http';
import { AuthInterceptor } from './Auth/interceptor';
import { ReactiveFormsModule,FormsModule } from '@angular/forms';
import { UploadprojectComponent } from './uploadproject/uploadproject.component';
import { CohortsComponent } from './cohorts/cohorts.component';
import { StylesComponent } from './styles/styles.component';
import { SingleProjectComponent } from './single-project/single-project.component';
import { UserProfileComponent } from './user-profile/user-profile.component';
import { CohortProfileComponent } from './cohort-profile/cohort-profile.component';
import { AndroidComponent } from './android/android.component';
import { FullstackComponent } from './fullstack/fullstack.component';
import { CohortProjectsComponent } from './cohort/cohort.component';


@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    HomeComponent,
    ProjectPageComponent,
    SignupComponent,
    LoginComponent,
    StudentProfileComponent,
    UploadprojectComponent, 
    ProfileComponent,
    CohortsComponent,
    StylesComponent,
    SingleProjectComponent,
    UserProfileComponent,
    CohortProfileComponent,
    AndroidComponent,
    FullstackComponent,
    CohortProjectsComponent,
  ],
  imports: [
    BrowserModule,
    ReactiveFormsModule,  
    HttpClientModule,
    AppRoutingModule,
    ReactiveFormsModule,
    FormsModule
  ],
  providers: [{
    provide: HTTP_INTERCEPTORS,
    useClass: AuthInterceptor,
    multi: true
  }],
  
  bootstrap: [AppComponent]
})
export class AppModule { }
