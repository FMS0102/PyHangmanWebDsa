// Adiciona event listeners para redimensionamento da janela e carregamento do documento
window.addEventListener("resize", resizeCanvas, false);
window.addEventListener("DOMContentLoaded", onLoad, false);

// Verifica se o navegador suporta requestAnimationFrame e, se não, fornece uma implementação alternativa
window.requestAnimationFrame =
    window.requestAnimationFrame ||
    window.webkitRequestAnimationFrame ||
    window.mozRequestAnimationFrame ||
    window.oRequestAnimationFrame ||
    window.msRequestAnimationFrame ||
    function (callback) {
        window.setTimeout(callback, 1000 / 60);
    };

// Declaração das variáveis globais
var canvas, ctx, w, h, particles = [], probability = 0.04,
    xPoint, yPoint;

// Função chamada quando o documento termina de carregar
function onLoad() {
    // Obtém o elemento canvas e o contexto 2D
    canvas = document.getElementById("canvas");
    ctx = canvas.getContext("2d");
    // Redimensiona o canvas para preencher a janela
    resizeCanvas();
    // Inicia a animação
    window.requestAnimationFrame(updateWorld);
}

// Função para redimensionar o canvas
function resizeCanvas() {
    if (!!canvas) {
        w = canvas.width = window.innerWidth;
        h = canvas.height = window.innerHeight;
    }
}

// Função principal responsável por atualizar e renderizar o mundo
function updateWorld() {
    update(); // Atualiza o estado das partículas
    paint(); // Renderiza o estado atual das partículas
    window.requestAnimationFrame(updateWorld); // Chama recursivamente a próxima atualização
}

// Função para atualizar o estado das partículas
function update() {
    if (particles.length < 500 && Math.random() < probability) {
        createFirework(); // Cria novos fogos de artifício com base na probabilidade
    }
    var alive = [];
    for (var i = 0; i < particles.length; i++) {
        if (particles[i].move()) {
            alive.push(particles[i]); // Remove partículas mortas
        }
    }
    particles = alive; // Atualiza a lista de partículas vivas
}

// Função para renderizar o estado atual das partículas
function paint() {
    ctx.clearRect(0, 0, w, h); // Limpa o canvas
    ctx.globalCompositeOperation = 'source-over'; // Define a operação de composição para padrão
    ctx.fillStyle = "rgba(0, 0, 0, 0.2)"; // Define a cor de fundo do canvas
    ctx.fillRect(0, 0, w, h); // Desenha um retângulo preenchido com a cor de fundo
    ctx.globalCompositeOperation = 'lighter'; // Define a operação de composição para mais claro
    for (var i = 0; i < particles.length; i++) {
        particles[i].draw(ctx); // Renderiza cada partícula
    }
}

// Função para criar um novo fogo de artifício
function createFirework() {
    xPoint = Math.random() * (w - 200) + 100;
    yPoint = Math.random() * (h - 200) + 100;
    var nFire = Math.random() * 50 + 100;
    var c = "rgb(" + (~~(Math.random() * 200 + 55)) + ","
        + (~~(Math.random() * 200 + 55)) + "," + (~~(Math.random() * 200 + 55)) + ")";
    for (var i = 0; i < nFire; i++) {
        var particle = new Particle();
        particle.color = c;
        var vy = Math.sqrt(25 - particle.vx * particle.vx);
        if (Math.abs(particle.vy) > vy) {
            particle.vy = particle.vy > 0 ? vy : -vy;
        }
        particles.push(particle); // Adiciona a partícula à lista
    }
}

// Definição do construtor de partículas
function Particle() {
    this.w = this.h = Math.random() * 4 + 1;
    this.x = xPoint - this.w / 2;
    this.y = yPoint - this.h / 2;
    this.vx = (Math.random() - 0.5) * 10;
    this.vy = (Math.random() - 0.5) * 10;
    this.alpha = Math.random() * .5 + .5;
    this.color;
}

// Protótipo de partícula com métodos move e draw
Particle.prototype = {
    gravity: 0.05,
    move: function () {
        this.x += this.vx;
        this.vy += this.gravity;
        this.y += this.vy;
        this.alpha -= 0.01;
        return !(this.x <= -this.w || this.x >= w || this.y >= h || this.alpha <= 0);
    },
    draw: function (c) {
        c.save();
        c.beginPath();
        c.translate(this.x + this.w / 2, this.y + this.h / 2);
        c.arc(0, 0, this.w, 0, Math.PI * 2);
        c.fillStyle = this.color;
        c.globalAlpha = this.alpha;
        c.closePath();
        c.fill();
        c.restore();
    }
};
