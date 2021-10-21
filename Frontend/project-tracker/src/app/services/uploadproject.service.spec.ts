import { TestBed } from '@angular/core/testing';

import { UploadprojectService } from './uploadproject.service';

describe('UploadprojectService', () => {
  let service: UploadprojectService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(UploadprojectService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
