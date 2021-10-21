import { Proj } from './../../../models/proj';
import { ActivatedRoute, Router } from '@angular/router';
import { UploadprojectService } from './../services/uploadproject.service';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';

@Component({
  selector: 'app-uploadproject',
  templateUrl: './uploadproject.component.html',
  styleUrls: ['./uploadproject.component.css']
})
export class UploadprojectComponent implements OnInit {

    formData = new Proj('','','','','')
    

  constructor(
    private UploadprojectService: UploadprojectService,
    private route: ActivatedRoute,
    private router: Router
  ) { }

  ngOnInit(): void {
  }
  addProject(){
  this.UploadprojectService.uploadProject(this.formData).subscribe(data =>{
    console.log(data)
    this.router.navigate(['projects']);
  })
}
}
