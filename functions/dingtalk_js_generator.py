def is_workday(api_key):
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


def kill_dingtalk():
    return '''function KillDingTalk(){
    // 结束钉钉进程
    app.openAppSetting("com.alibaba.android.rimet");  // 打开钉钉app详情页

    // 等待并点击“结束运行”按钮
    var stopButton = desc("结束运行").findOne();  // 等待找到结束运行的文本
    if (stopButton.isEnabled()) {
        stopButton.click();  // 点击“结束运行”
    }else{
        return 0
    }

    // 等待并点击“确定”按钮
    var confirmButton = text("确定").findOne();  // 等待找到确定按钮
    confirmButton.click();  // 点击“确定”
}


'''


def open_check_in_page():
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


def start_check_in():
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


def trip_check():
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


def autojs_main(api_key:str, show_console:bool, is_trip_check:bool):
    show_console_code = ''
    workday_code = ''
    trip_check_code = ''

    if show_console:
        show_console_code = show_console_log()

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
%s%s
    // 获取屏幕尺寸
    var screenWidth = device.width;
    var screenHeight = device.height;

    KillDingTalk();                     // 结束钉钉进程
    OpenCheckInPage(companyName, 50);   // 打开打卡页面，部分手机需要多次尝试，可适当调整尝试次数
    StartCheckIn(companyName, screenWidth, screenHeight);       // 开始打卡
    %s
}


''' % (show_console_code, workday_code, trip_check_code)

    return result


def show_console_log():
    return """
    console.show();
"""

def gen_dingtalk_js(setting_json: dict):
    result = ''

    if setting_json.get('apihubToken'):     # 追加是否工作日的判断
        result += is_workday(setting_json.get('apihubToken'))

    result += kill_dingtalk()               # 追加结束钉钉进程的代码
    result += open_check_in_page()          # 追加打开打卡页面的代码
    result += start_check_in()              # 追加开始打卡的代码
    
    if setting_json.get('tripCheck'):       # 追加外勤打卡的代码
        result += trip_check()

    # 生成主流程代码
    is_show_console = setting_json.get('showConsole')
    is_trip_check = setting_json.get('tripCheck')
    result += autojs_main(setting_json.get('apihubToken'), is_show_console, is_trip_check)

    result += 'start("%s");' % setting_json.get('companyName')  # 追加启动代码

    return result
