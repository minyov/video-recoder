Environment Variables
======
`DJANGO_DEVELOPMENT` - development  
`DJANGO_TEST` - testing  
`No DJANGO_DEVELOPMENT and no DJANGO_TEST` - production

Scripts
======
Run tests: `python3 manage.py test apps`  
Deploy to kubernetes cluster: `deploy/kubernetes/deploy.sh`  
Delete from kubernetes cluster: `deploy/kubernetes/delete.sh`

Requirements
======
```bash
Django==3.0.6
djangorestframework==3.11.0
mysqlclient==1.4.6
celery==4.4.2
Pillow==7.1.2
opencv-python==4.2.0.34
ffmpeg-python==0.2.0
requests==2.23.0
uwsgi==2.0.18
```
