CFLAGS=-std=c11 -g -static

9cc: 9cc.c

test: 9cc
	./test.sh

clean:
	rm -f 9cc *.o *~ tmp*

.PHONY: test clean

docker:
	docker run -it --rm --platform=linux/amd64 -v $(pwd):/cc ubuntu
