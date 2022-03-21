<h1>Web Terminal For Docker</h1>


<p>1, git clone https://github.com/lanbiter/Docker-console.git</p>
<p>2, pip install -r requirements.txt</p>
<p>3, edit /etc/default/docker add DOCKER_OPTIONS="-H unix:///var/run/docker.sock -H 0.0.0.0:2375" or /etc/sysconfig/docker-network,add  DOCKER_NETWORK_OPTIONS="-H unix:///var/run/docker.sock -H 0.0.0.0:2375" or /lib/systemd/system/docker.service ,and then restart docker service</p>
<p>4, vim configure.py</p>
<p>5, fix DOCKER_HOST and DOCKER_API_VERSION according to your own situation and set timeout</p>
<p>6, choice a containerID(running) in you DOCKER_HOST and set CONTAINER_ID</p>
<p>7, execute start.sh and visit http://(website):5000/</p>
<hr>
<img src='static/show.png'>


打赏：


![image](https://user-images.githubusercontent.com/10483310/159258692-ba76ccea-7a96-4aac-8b28-77f9e4d3a775.png)
