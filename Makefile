ALLINONE_SRC := $(shell find allinone -print )

.allinone.iid: $(ALLINONE_SRC)
	docker build --iidfile $@ \
		--build-arg=DOCKER_PREFIX=$(DOCKER_PREFIX) \
		--build-arg=http_proxy=$(http_proxy) \
		--build-arg=https_proxy=$(https_proxy) \
		--build-arg=MAVEN_REPO=$(MAVEN_REPO) \
		--build-arg=IVY_REPO=$(IVY_REPO) \
		allinone

run-allinone: .allinone.iid
	docker -it --privileged \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-v /usr/bin/docker:/usr/bin/docker:ro \
		-v /sys/fs/cgroup:/sys/fs/cgroup \
	 run $(shell cat $<)
