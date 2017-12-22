ALLINONE_SRC := $(shell find allinone -print )

BUILD_CONCURRENCY ?= 1

.allinone.iid: $(ALLINONE_SRC)
	docker build --iidfile $@ \
		--build-arg=DOCKER_PREFIX=$(DOCKER_PREFIX) \
		--build-arg=http_proxy=$(http_proxy) \
		--build-arg=https_proxy=$(https_proxy) \
		--build-arg=MAVEN_REPO=$(MAVEN_REPO) \
		--build-arg=IVY_REPO=$(IVY_REPO) \
		--build-arg=BUILD_CONCURRENCY=$(BUILD_CONCURRENCY) \
		allinone

run-allinone: .allinone.iid
	docker run -it --privileged \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-v /usr/bin/docker:/usr/bin/docker:ro \
		-v /sys/fs/cgroup:/sys/fs/cgroup \
		$(shell cat $<)
