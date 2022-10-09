/* 登录名校验 */
export function loginNameValidator(rule, value, callback){
    const reg= /^[a-zA-Z][\w-. @]*$/;
    if(value == '' || value == undefined || value == null){
      callback();
    }else {  
      if (!reg.test(value)){
        callback(new Error('要求为：英文字母开头，后续为字母数字及_-. @符号'));
      }else {
        callback();
      }
    }
  }