$(window).resize(function() {
    $(".faded-background").width(
        Math.ceil($(".main-image").width())
      );
    $(".shrink").width(
        Math.ceil($(".native").width())
      );

    $(".back-fill").width(
        Math.ceil($(".native").width())
    );

    // if window is small, set the width of images in the slider to be window size
     if (window.innerWidth < 520) {
      $('.slick-slide').css("max-width", (window.innerWidth - 10).toString() + "px");
    }
});

window.onload = function() {

    $(".faded-background").width(
        Math.ceil($(".main-image").width())
      );

    $(".shrink").width(
        Math.ceil($(".native").width())
      );
    
    $(".back-fill").width(
        Math.ceil($(".native").width())
      );

    // initialize the carousel element 
    $('.slider').slick({
      centerMode: true,
      centerPadding: '10px',
      autoplay: true,
      autoplaySpeed: 3500,
      dots: true,
      slidesToShow: 1,
      variableWidth: true,
      appendArrows: '.slider',
      nextArrow: '.right-btn',
      prevArrow: '.left-btn',
      responsive: [
      {
          breakpoint: 768,
          settings: {
            arrows: false,
            centerMode: true,
            centerPadding: '10px',
            slidesToShow: 1
        }
    },
    {
      breakpoint: 480,
      settings: {
        arrows: false,
        centerMode: true,
        centerPadding: '10px',
        slidesToShow: 1
    }}]});

     if (window.innerWidth < 520) {
      $('.slick-slide').css("max-width", (window.innerWidth - 10).toString() + "px");
    }
};

function displayShare() {
  if ($('#share-details').css("visibility") != "visible") {
    $('#share-details').css("visibility", "visible");

    if ($('#qrcode').is(':empty')) {
      // make a new qr code 
      let qrcode = new QRCode(document.getElementById("qrcode"), {
        text: $("#loc").text(),
        width: 128,
        height: 128,
        colorDark : "#000000",
        colorLight : "#ffffff",
        correctLevel : QRCode.CorrectLevel.H
      });
    }

    $("#qrcode").css("width", "128px");
    $("#qrcode").css("height", "128px");
    $("#share").css("display", "none");
  }  
}


// copy text or image
function SelectText(element) {

  if (document.body.createTextRange) {

    let range = document.body.createTextRange();
    range.moveToElementText(element);
    range.select();

  } else if (window.getSelection) {

      let selection = window.getSelection();
      let range = document.createRange();
      range.selectNodeContents(element);
      selection.removeAllRanges();
      selection.addRange(range);
    }
}

$(".copyable").click(function() {
            
  $(this).attr("contenteditable", true);
    SelectText(this);
    document.execCommand('copy');
    window.getSelection().removeAllRanges();
    $(this).removeAttr("contenteditable");
    alert("Copied to clipboard!");
});


// reveal the frame when loading is done 
Pace.on("done", () => {
    $(".container-fluid").removeClass("hidden");
});
