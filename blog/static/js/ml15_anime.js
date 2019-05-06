anime.timeline({loop: true})
    .add({
        targets: '.ml15 .word',
        scale: [2, 1],
        opacity: [0, 1],
        easing: "easeOutCirc",
        duration: 800,
        delay: function (el, i) {
            return 800 * i;
        }
    }).add({
    targets: '.ml15',
    opacity: 0,
    duration: 1000,
    easing: "easeOutExpo",
    delay: 1000
});


$.fx.step.textShadowBlur = function (fx) {
    $(fx.elem)
        .prop('textShadowBlur', fx.now)
        .css({textShadow: '0 0 ' + Math.floor(fx.now) + 'px black'});
};
;