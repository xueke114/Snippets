/*
方案二是采用crt文件的方式

crt下载源
https://github.com/q3aql/aria2-static-builds
 */

#include <aria2/aria2.h>
int main() {
  // 设置session的opions
  aria2::KeyVals sessionOptions;
#ifdef _WIN32
  sessionOptions.push_back({"ca-certificate", "ca-certificates.crt"});
#endif
  // 创建一个session，采用自定义的options和Config
  aria2::Session *session = aria2::sessionNew(sessionOptions, sessionConfig);
}
