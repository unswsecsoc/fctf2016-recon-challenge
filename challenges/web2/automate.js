console.log("[+] Initialising");

var page = require('webpage').create();
var host = "localhost:5000";
var url = "http://"+host+"/livingdead";
var secretpassage = "http://"+ host + "/secretpassage";
var timeout = 2000;
var util = require('util');
var interval = 0;
var loadInProgress = false;

page.settings.userAgent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36';
page.settings.javascriptEnabled = true;

phantom.cookiesEnabled = true;
phantom.javascriptEnabled = true;

page.addCookie({
  'name': 'Flag',
  'value': 'FLAG{w0w_d0nt_y0u_l0v3_m0_ke_pon}',
  'domain': host,
  'path': '/',
  'httponly': false
});
// page.onNavigationRequested = function(url, type, willNavigate, main) {
//   console.log("[URL] URL="+url);
// };

page.settings.resourceTimeout = timeout;
page.onResourceTimeout = function(e) {
  setTimeout(function(){
    console.log("[+] Timeout")
    phantom.exit();
  }, 500);
};
var links = []
console.log("[+] Starting Automate");

function process() {
    console.log("[+] Starting on processing");
    if (links.length == 0) {
        console.log("[+] Done");
        phantom.exit();
    } else {
        //remove the first item of an array
        url = links.shift();
        var currentUrl = url
        console.log("   [+] Starting " + url);
        page = require('webpage').create();
        page.addCookie({
          'name': 'Flag',
          'value': 'FLAG{w0w_d0nt_y0u_l0v3_m0_ke_pon}',
          'domain': host,
          'path': '/',
          'httponly': false
        });
        page.open(url, secretpage);
    }
}
function secretpage(status) {
    console.log("   [+] Starting " + secretpassage);
    page.open(secretpassage, onFinishedLoadingStage);
}

function onFinishedLoadingStage(status) {
    console.log("   [-] Finished " + url);
    // console.log(status);
    page.close()
    process();
}


var stage2 = function() {
    page.open(url, function(status) {
      console.log("[+] Visitng " + url);
      links = page.evaluate(function() {
        return [].map.call(document.querySelectorAll('a'), function(link) {
          return link.getAttribute('href');
        });
      });
      setTimeout(function(){
        process();
      }, 500);
    });
}

stage2();
// page.open(login, function(){
//   console.log("[+] Trying to log in");
//   // page.includeJs(
//     // Include the https version, you can change this to http if you like.
//     // 'https://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js',
//     // function() {
//   page.evaluate(function() {
//     // jQuery is loaded, now manipulate the DOM
//     console.log("[+] Opening the loginpage");
//     // var loginForm = $('form#login');
//     $('form#login').find('input[name="username"]').value ='pokechampion';
//     $('form#login').find('input[name="password"]').value ='dontyoulovelongpasswords';
//     $('form#login').submit();

//     return document.querySelectorAll("html")[0].outerHTML;

//   });
//   interval = setInterval(function(){
//     if(!loadInProgress) {
//         page.open(url, function(status) {
//             if(status === 'success') {

//                 console.log("[+] Trying to get the cookies");
//                 console.log(util.inspect(page.cookies, {showHidden: false, depth: null}));
//                 console.log(util.inspect(phantom.cookies, {showHidden: false, depth: null}));
//                 // console.log(page.content)
//             } else {
//                 console.log('error');
//             }
//             phantom.exit();
//         });
//         clearInterval(interval);
//     }
//   },50);
//     // console.log(page.cookies);
//     // console.log(phantom.cookies);
//     // }
//   // );
//     // phantom.exit();
//   // setTimeout(function () {

//   //   stage2();
//   // }, 1000);
// });
