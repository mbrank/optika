#include "vec3.h"
#include <iostream>

int main()
{
  vec3 c;
  for (int i = 0; i < 10000000; ++i) {
    vec3 a = vec3(i, 2, 3);
	vec3 b = vec3(i, 2, 3);
	c = a+b;
  }
  std::cout << c.x() << " new\n";

  return 0;
}

