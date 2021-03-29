#include <iostream>
#include </home/brankm/eigen/Eigen/Dense>
 
using Eigen::MatrixXd;
using Eigen::VectorXd;
using Eigen::Vector2d;
using namespace Eigen;
int main()
{
  MatrixXd m(2,2);
  m(0,0) = 3;
  m(1,0) = 2.5;
  m(0,1) = -1;
  m(1,1) = m(1,0) + m(0,1);
  Vector2d v(1,2), g(3,4);
  ArrayXf a(3);
  a << 1,2,3;
  ArrayXf b(3);
  b << 1,2,3;
  //std::cout << "test";
  //std::cout << g.transpose() << "\n";
  //std::cout << "test00";
  //std::cout << v.array() << std::endl;
  //std::cout << "test01";
  //std::cout << g.array() << std::endl;
  //std::cout << "test1\n";
  //std::cout << v*g.transpose() << std::endl;
  //std::cout << "test2\n";
  //std::cout << a*b << std::endl;
  //std::cout << v*g << std::endl;
  // Image
  
  const int image_width = 256;
  const int image_height = 256;
  
  // Render
  
  std::cout << "P3\n" << image_width << ' ' << image_height << "\n255\n";
  
  for (int j = image_height-1; j >= 0; --j) {
	for (int i = 0; i < image_width; ++i) {
	  auto r = double(i) / (image_width-1);
	  auto g = double(j) / (image_height-1);
	  auto b = 0.25;
	  
	  int ir = static_cast<int>(255.999 * r);
	  int ig = static_cast<int>(255.999 * g);
	  int ib = static_cast<int>(255.999 * b);
	  
	  std::cout << ir << ' ' << ig << ' ' << ib << '\n';
	}
  }
}
