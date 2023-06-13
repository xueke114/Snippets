/*
方案一比较暴力，直接取消对https证书的认证
 */

#include <aria2/aria2.h>
int main() {
  // 设置session的opions
  aria2::KeyVals sessionOptions;
#ifdef _WIN32
  sessionOptions.push_back({"check-certificate", "false"});
#endif
  // 创建一个session，采用自定义的options和Config
  aria2::Session *session = aria2::sessionNew(sessionOptions, sessionConfig);
}
