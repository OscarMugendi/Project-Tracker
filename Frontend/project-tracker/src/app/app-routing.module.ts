
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Routes, RouterModule } from '@angular/router';

import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { SignupComponent } from './signup/signup.component';
import { ProjectPageComponent } from './project-page/project-page.component';
import { StudentProfileComponent } from './student-profile/student-profile.component';
import { AuthGuard } from './auth.guard';
import { UploadprojectComponent } from './uploadproject/uploadproject.component';
import { ProfileComponent } from './profile/profile.component';
import { CohortsComponent } from './cohorts/cohorts.component';
import { StylesComponent } from './styles/styles.component';
import { SingleProjectComponent } from './single-project/single-project.component';
import { UserProfileComponent } from './user-profile/user-profile.component';
import { CohortProfileComponent } from './cohort-profile/cohort-profile.component';
import { AndroidComponent } from './android/android.component';
import { FullstackComponent } from './fullstack/fullstack.component';
import { CohortProjectsComponent } from './cohort/cohort.component';

const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'signup', component: SignupComponent },
  { path: 'home', component: HomeComponent },

 
  { path: 'add-projects', component:UploadprojectComponent },
 
 
  { path: 'cohorts', component:CohortsComponent },


  { path: 'projects',
    children: [
      { path: '', component: ProjectPageComponent },
      { path: ':id', component: SingleProjectComponent },
    ]
  },
  { path: 'profile', component:StudentProfileComponent,canActivate:[AuthGuard] },
 
  { path: 'profiles',
    children: [
      { path: '', component: ProfileComponent },
      { path: ':id', component: UserProfileComponent },
    ]
  },
  { path: 'cohorts',
    children: [
      { path: '', component: CohortsComponent },
      { path: ':id', component: CohortProfileComponent },
    ]
  },

  { path: 'styles', component:StylesComponent },
  { path: 'android', component: AndroidComponent },
  { path: 'fullstack', component: FullstackComponent },
  { path: 'cohort', component: CohortProjectsComponent },
];


@NgModule({
  declarations: [],
  imports: [
    CommonModule,

    RouterModule.forRoot(routes, { useHash: true })

  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }

