release: btotrace.exe
debug: ctrace.exe

ctrace.exe: main.c vector.c ray.c sphere.c constants.c hittable.c hittable_list.c camera.c rtweekend.c color.c
	gcc -g -fsanitize=address -fsanitize=undefined -Wall -Wextra -o ctrace main.c vector.c ray.c sphere.c constants.c hittable.c hittable_list.c camera.c rtweekend.c color.c -lm
	#-g -fsanitize=address -fsanitize=undefined -Wall -Wextra


btotrace.exe: main.c vector.c ray.c sphere.c constants.c hittable.c hittable_list.c camera.c rtweekend.c color.c
	gcc -O3 -ffast-math -o $@ $^ -lm

clean:
	rm *.exe *.ppm
