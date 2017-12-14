


# logstash setup

## for ARM (rasp pi)

```bash
sudo update-java-alternatives -s jdk-8-oracle-arm32-vfp-hflt
```

```bash
sudo apt install ant texinfo build-essential
git clone https://github.com/jnr/jffi.git ~/src/jffi
cd ~/src/jffi
time ant jar
sudo mv -n /usr/share/logstash/vendor/jruby/lib/jni/arm-Linux/libjffi-1.2{.so,.so.old}
sudo cp -i build/jni/libjffi-1.2.so /usr/share/logstash/vendor/jruby/lib/jni/arm-Linux/
```


## for all linux (including ARM)

```bash
wget https://artifacts.elastic.co/downloads/logstash/logstash-5.6.5.deb
sudo dpkg -i logstash-5.6.5.deb

echo '
logger.cgroupjunk.name = logstash.instrument.periodicpoller.cgroup
logger.cgroupjunk.level = info

' >> /etc/logstash/log4j2.properties
```


# logstash config

```bash
copy conf.d/*.conf files to /etc/logstash/conf.d/
copy conf.d/.sqs-credentials.yml.sample to /etc/logstash/conf.d/.sqs-credentials.yml
tweak credentials accordingly
```

## dealing with life

```bash
sudo tail -f /var/log/logstash/*.log
sudo systemctl is-enabled logstash.service
sudo systemctl enable logstash.service
sudo systemctl stop logstash.service
sudo systemctl start logstash.service
sudo systemctl restart logstash.service
```
