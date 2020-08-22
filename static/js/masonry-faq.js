// gets all the bricks
var bricks = document.getElementsByClassName('item');

var content = [
    {
        question: 'What do the notices look like?',
        answer: `Sign up and <a style='text-decoration: underline !important; ' href='/#subscribe'>take a look for yourself!</a>. If it isn't your taste, you can always unsubscribe.`
    },

    {
        question: 'When are the notices sent?',
        answer: "7:30am, give or take a few minutes. "
    },

    {
        question: 'How does this app work?',
        answer: "The app is a stylised web scraper/aggregator, run with Python. The notices are taken from the parent portal and reformatted a newsletter. If you are interested in the code, come to programming club and we can explain it to you."
    },

    {
        question: 'What happens if a notice is added after the email is sent?',
        answer: "The notice will be on tommorrow's email, due to the limitations of the app."
    },

    {
        question: "Does this work for the parent portals at other schools?",
        answer: "Yes it does, as long as it runs off Kamar! If you want more information, email <u><a href='mailto:ncdaily@newlands.school.nz'>ncdaily@newlands.school.nz</a></u>"
    },

    {
        question: "Does this change anything with the old notices?",
        answer: "Nope! NC Daily is an add-on and the teachers don't need to learn anything new. It just takes existing information and reformats it."
    }
]

// gives transition times
var extraTime = 0
for (var i = 0; i < bricks.length; i++) {
  bricks[i].style.transition = 'all ' + (0.5 + extraTime) + 's';
  extraTime += 0.4;
  bricks[i].addEventListener("webkitAnimationEnd", fillColor);
  bricks[i].addEventListener("animationend", fillColor);
  bricks[i].addEventListener("oanimationend", fillColor);
}

function fillColor() {
    var colors = ['#41b9e1', '#419ee1', '#4169e1', '#6941e1', '#9141e1', '#e141b9'];
    // var colors = ['#41b9e1'];
    for (var i = 0; i < bricks.length; i++) {
    bricks[i].style.background = colors[i % colors.length];
    bricks[i].innerHTML = '<div style="display: flex"><h3>' + content[i]['question'] + '</h3>' + '<i class="fas fa-chevron-down"></i></div>' + '<p class="content">' + content[i]['answer'] + '</p>';
  }
}

var coll = document.getElementsByClassName("item");


for (var i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var question = this.firstChild;
    var content = this.lastChild;

    var masonry = document.querySelector('.masonry');

    if (content.style.height){
        content.style.height = null;
        question.lastChild.classList.remove('fa-chevron-up');
        question.lastChild.classList.add('fa-chevron-down');
        // masonry.style.height = (parseInt(masonry.clientHeight, 10) - parseInt(content.style.maxHeight, 10)) + 'px';
    } else {
        content.style.height = content.scrollHeight + 'px' ;
        question.lastChild.classList.remove('fa-chevron-down');
        question.lastChild.classList.add('fa-chevron-up');
        // masonry.style.height = parseInt(masonry.clientHeight, 10) + parseInt(content.style.maxHeight, 10) + 'px';
    }
    });
}