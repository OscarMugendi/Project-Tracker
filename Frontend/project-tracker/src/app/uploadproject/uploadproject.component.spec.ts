import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UploadprojectComponent } from './uploadproject.component';

describe('UploadprojectComponent', () => {
  let component: UploadprojectComponent;
  let fixture: ComponentFixture<UploadprojectComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UploadprojectComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UploadprojectComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

function beforeEach(arg0: () => Promise<void>) {
  throw new Error('Function not implemented.');
}


function expect(component: ProjectFormComponent) {
  throw new Error('Function not implemented.');
}
