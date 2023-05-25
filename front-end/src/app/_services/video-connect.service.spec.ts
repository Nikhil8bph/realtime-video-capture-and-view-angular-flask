import { TestBed } from '@angular/core/testing';

import { VideoConnectService } from './video-connect.service';

describe('VideoConnectService', () => {
  let service: VideoConnectService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(VideoConnectService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
