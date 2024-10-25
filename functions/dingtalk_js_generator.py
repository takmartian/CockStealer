# This file is used to generate the AutoJS script for DingTalk check-in
# The script is generated in JavaScript based on the settings provided by the user


class DingTalkJSGenerator:
    def __init__(self, setting_json: dict):
        self.setting_json = setting_json
        self.is_unlock_phone = self.setting_json.get('unlockPhone')
        self.unlock_method = setting_json.get('unlockMethod')
        self.unlock_password = setting_json.get('unlockPassword')
        self.company_name = setting_json.get('companyName')
        self.is_show_console = setting_json.get('showConsole')
        self.is_trip_check = setting_json.get('tripCheck')
        self.apihub_token = setting_json.get('apihubToken')

    def unlock_phone(self):
        """
        生成解锁手机的代码
        :return: 解锁手机的代码
        """
        return '''function unlockPhone(mode, password) {
    // 获取屏幕宽高
    let screenWidth = device.width;
    let screenHeight = device.height;

    // 上划解锁屏幕
    swipe(500,2000,500,1000,210);
    sleep(500);

    if (mode === "noPassword") {
        console.log("直接上划解锁");
    }
    else if (mode === "passwordUnlock") {
        console.log("上划后自动输入数字密码解锁");

        // 依次输入密码
        for(var i = 0; i < password.length; i++) {
            var p = text(password[i].toString()).findOne().bounds();
            click(p.centerX(), p.centerY());
            sleep(100);
        }
    }
    else if (mode === "patternUnlock") {
        console.log("上划后自动进行手势解锁");

        // 设定九宫格的点位（假设3x3的九宫格）
        let points = [
            [screenWidth * 0.23, screenHeight * 0.59],  // 点1
            [screenWidth * 0.5, screenHeight * 0.59],  // 点2
            [screenWidth * 0.77, screenHeight * 0.59],  // 点3
            [screenWidth * 0.23, screenHeight * 0.72],  // 点4
            [screenWidth * 0.5, screenHeight * 0.72],  // 点5
            [screenWidth * 0.77, screenHeight * 0.72],  // 点6
            [screenWidth * 0.23, screenHeight * 0.85],  // 点7
            [screenWidth * 0.5, screenHeight * 0.85],  // 点8
            [screenWidth * 0.77, screenHeight * 0.85]   // 点9
        ];

        // 手势密码划动路径
        let gesturePath = [];
        for (let i = 0; i < password.length; i++) {
            let pointIndex = parseInt(password[i]) - 1;
            gesturePath.push(points[pointIndex]);
        }

        // 执行手势划动
        print(gesturePath)
        gesture(5000, gesturePath);
    } else {
        console.log("无效的解锁模式");
    }
}


'''

    def is_workday(self, api_key):
        """
        生成判断是否工作日的代码
        :param api_key: apiHub的API Key
        :return: 判断是否工作日的代码
        """
        return '''function GetNowDate(){
    // 获取当前日期，格式YYYYMMDD
    var date = new Date();
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var day = date.getDate();

    // 年月日强制转换为字符串
    year = year + '';
    month = month + '';
    day = day + '';

    var currentDate = year + (month < 10 ? '0' + month : month) + (day < 10 ? '0' + day : day);

    return currentDate
}


function IsWorkday() {
    // 是否工作日，返回true/false
    var url = "https://api.apihubs.cn/holiday/get?api_key=" + "%s" + "&field=workday&date=" + GetNowDate();
    var isWorkday = null;
    var maxRetries = 5;  // 设置最大重试次数，防止无限循环
    var attempt = 0;
  
    while (isWorkday === null && attempt < maxRetries) {
      try {
        var res = http.get(url);
        var dateDetail = res.body.json();
        isWorkday = dateDetail.data.list[0].workday;
      } catch (error) {
        log("请求失败，正在重试... 尝试次数: " + (attempt + 1));
        attempt++;
      }
    }
  
    if (isWorkday === null) {
      log("请求失败，已达到最大重试次数。");
      exit();
    }
  
    isWorkday = (isWorkday === 1) ? true : false
  
    return isWorkday;
  }
  
  
  ''' % api_key

    def kill_dingtalk(self):
        """
        生成结束钉钉进程的代码
        :return: 结束钉钉进程的代码
        """
        return '''function KillDingTalk(){
  // 结束钉钉进程
  app.openAppSetting("com.alibaba.android.rimet");  // 打开钉钉app详情页

  // 等待并点击“结束运行”按钮
  while (true) {
    if (desc("结束运行").exists()) {
        break;
    }else{
        sleep(500);
    }
  }

  var stopButton = desc("结束运行").findOne();  // 找到结束运行的文本

  if (stopButton.isEnabled()) {
      stopButton.click();  // 点击“结束运行”
  }else{
      return 0
  }

  // 等待并点击“确定”按钮
  while (true) {
    if (text("确定").exists()) {
        break;
    }else{
        sleep(500);
    }
  }
  var confirmButton = text("确定").findOne();  // 等待找到确定按钮
  confirmButton.click();  // 点击“确定”
}


'''

    def open_check_in_page(self):
        """
        生成打开打卡页面的代码
        :return: 打开打卡页面的代码
        """
        return '''function OpenCheckInPage(companyName, maxRetries) {
    // 选择打卡企业页面
    let pageCheckIn = app.intent({
        action: "VIEW",
        data: "dingtalk://dingtalkclient/page/link?url=https://attend.dingtalk.com/attend/index.html"
    });
    app.startActivity(pageCheckIn);

    // 查找公司名称maxRetries次
    var curTry = 1
    while (curTry < maxRetries) {
        if (id("android:id/text1").text(companyName).exists()) {
            id("android:id/text1").text(companyName).click();
            break;
        }
        curTry++;
        log("找不到公司，重试第" + curTry + "次");
        sleep(500);
    }
}


'''

    def start_check_in(self):
        """
        生成开始打卡的代码
        :return: 开始打卡的代码
        """
        return '''function StartCheckIn(companyName, width, height) {
    while (true) {
        if (id("com.alibaba.android.rimet:id/title_bar_name").text(companyName).exists()) {
            sleep(5000);
            break;
        }else{
            sleep(500);
        }
    }

    // 计算屏幕上 x:50% 和 y:60% 的坐标
    var x = width * 0.5;   // 50% 宽度
    var y = height * 0.6;  // 60% 高度

    // 在计算出的坐标位置点击
    click(x, y);
}


'''

    def trip_check(self):
        """
        生成外勤打卡的代码
        :return: 外勤打卡的代码
        """
        return '''function TripCheck(width, height) {
    while (true) {
        if (id("com.alibaba.android.rimet:id/title_bar_name").text("外勤打卡").exists()) {
            sleep(5000);
            break;
        }else{
            sleep(500);
        }
    }

    // 计算屏幕上 x:50% 和 y:60% 的坐标
    var x = width * 0.5;   // 50% 宽度
    var y = height * 0.9;  // 90% 高度

    // 在计算出的坐标位置点击
    click(x, y);
}


'''

    def autojs_main(self, is_unlock_phone: bool, api_key: str, show_console: bool, is_trip_check: bool,
                    unlock_mode: str, unlock_password: str):
        """
        生成AutoJS主函数代码
        :param api_key: apiHub的API Key
        :param show_console: 是否显示控制台
        :param is_trip_check: 是否外勤打卡
        :return: 生成的AutoJS主函数代码
        """
        show_console_code = ''
        unlock_phone_code = ''
        workday_code = ''
        trip_check_code = ''

        if is_unlock_phone:
            unlock_phone_code = """
    // 解锁手机
    unlockPhone('%s', '%s');
    """ % (unlock_mode, unlock_password)

        if show_console:
            show_console_code = self.show_console_log()

        if api_key:
            workday_code = """
    // 判断是否工作日
    if (!IsWorkday()) {
        log("今天不用上班");
        exit();
    }
"""

        if is_trip_check:
            trip_check_code = '''TripCheck(screenWidth, screenHeight);  // 外勤打卡'''

        result = '''function start(companyName) {
    auto();     // 无障碍服务检查
    device.wakeUpIfNeeded();     // 唤醒设备
    device.keepScreenOn(3600 * 1000);   // 保持屏幕常亮，单位毫秒
%s%s%s
    // 获取屏幕尺寸
    var screenWidth = device.width;
    var screenHeight = device.height;

    KillDingTalk();                     // 结束钉钉进程
    sleep(2000);
    OpenCheckInPage(companyName, 50);   // 打开打卡页面，部分手机需要多次尝试，可适当调整尝试次数
    StartCheckIn(companyName, screenWidth, screenHeight);       // 开始打卡
    %s
    log("打卡完成");
    device.cancelKeepingAwake();    // 取消屏幕常亮
}


''' % (show_console_code, unlock_phone_code, workday_code, trip_check_code)

        return result

    def show_console_log(self):
        """
        生成显示控制台的代码
        :return: 显示控制台的代码
        """
        return """
    console.show();
"""

    def gen_dingtalk_js(self):
        """
        生成钉钉打卡脚本
        :return: 生成的钉钉打卡脚本
        """
        result = ''

        # 参数校验
        if self.is_unlock_phone and self.unlock_method is None:
            # 如果需要解锁手机，但是没有选择解锁方式
            return '请选择解锁方式'

        if self.is_unlock_phone and (
                self.unlock_method == 'passwordUnlock' or self.unlock_method == 'patternUnlock') and not self.unlock_password:
            # 如果需要解锁手机，但是没有填写解锁密码
            return '请填写解锁密码'

        if not self.company_name:
            # 如果没有填写公司名称
            return '请填写钉钉上的完整公司名称'

        if self.is_unlock_phone:
            # 如果需要解锁手机，追加解锁手机的代码
            result += self.unlock_phone()

        if self.apihub_token:
            # 如果填写了apiHub的API Key，追加判断是否工作日的代码
            result += self.is_workday(self.apihub_token)

        # 生成主流程代码
        result += self.kill_dingtalk()  # 追加结束钉钉进程的代码
        result += self.open_check_in_page()  # 追加打开打卡页面的代码
        result += self.start_check_in()  # 追加开始打卡的代码

        if self.is_trip_check:  # 追加外勤打卡的代码
            result += self.trip_check()

        result += self.autojs_main(
            is_unlock_phone=self.is_unlock_phone,
            api_key=self.apihub_token,
            show_console=self.is_show_console,
            is_trip_check=self.is_trip_check,
            unlock_mode=self.unlock_method,
            unlock_password=self.unlock_password
        )

        result += 'start("%s");' % self.company_name  # 追加启动代码

        return result
