# Online Judge

This OJ was made to host the programming contest held in IIIT-Bh. It has 3 parts- Checker, Website backend frontend in django and jinja, Redis server(bridge b/w backend and checker).

## About OJ

**Architecture:**
3 docker containers connected on a bridge(docker).

- 1 container => Checker
- 2 container => Website backend frontend in django and jinja
- 3 container => Redis which acts as a connection stream between backend and checker

**Why to have a redis server as a middle bridge?**

Reason: Our aim was to create scalable setup, so that if number of submission increases we can spawn new checker container and connect them to redis, Each checker container has a unique id though which it registers on redis.

There are 2 queues in redis.

- 1st queue => outgoing from bdjango backend to checker container(s).
  Django backend as soon as it receives a submission pushes the code with correct answer into queue, from which checker takes a task and checks the code.
- 2nd queue => outgoing from checker to django backend.

Checker after checking the code, returns the status in redis queue which is received by django backend and given to user

**Why container for checker?**

Our aim was to isolate the checking process in order to reduce any damage from malicious submission, so we run the whole user submitted code in a container with least permission possible, and even if someone still manage to get our checker down, our django backend would be not effected and we can spawn checker container instantly.
