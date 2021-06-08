release: ctrace
debug: ctracedbg
random: ctracerandom

ctracedbg: main.c vector.c ray.c sphere.c constants.c hittable.c hittable_list.c camera.c rtweekend.c color.c
	gcc -g -fsanitize=address -fsanitize=undefined -Wall -Wextra -o ctrace main.c vector.c ray.c sphere.c constants.c hittable.c hittable_list.c camera.c rtweekend.c color.c -lm
        #-g -fsanitize=address -fsanitize=undefined -Wall -Wextra


ctrace: main.c vector.c ray.c sphere.c constants.c hittable.c hittable_list.c camera.c rtweekend.c color.c material.c
	clang -O3 -ffast-math -o $@ $^ -lm


ctracerandom: main_random.c vector.c ray.c sphere.c constants.c hittable.c hittable_list.c camera.c rtweekend.c color.c material.c
	clang -O3 -ffast-math -o $@ $^ -lm


clean:
	rm *.exe *.ppm
