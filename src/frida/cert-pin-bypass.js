// pin-bypass.js
Java.perform(function () {
  var CP = Java.use("okhttp3.CertificatePinner");

  // https://github.com/lysine-dev/okhttp/blob/75d8f91cfe2495b79d07b1dabe05789caa429ac2/okhttp/src/commonJvmAndroid/kotlin/okhttp3/CertificatePinner.kt#L157
  CP["check$okhttp_release"].overload(
    "java.lang.String",
    "kotlin.jvm.functions.Function0",
  ).implementation = function () {
    console.log("Bypassed");
    return;
  };
});
