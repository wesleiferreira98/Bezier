from PyQt5.QtWidgets import  QWidget
from PyQt5.QtGui import QPainter, QPen, QPolygonF,QColor
from PyQt5.QtCore import Qt, QPoint,QRect,QTimer
class BezierCurveWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.num_points = 4  # Número padrão de pontos de controle
        self.points = [QPoint(50, 200), QPoint(150, 50), QPoint(250, 250), QPoint(350, 200)]
        self.current_point_index = 0
        self.selected_point = None
        self.setMinimumSize(800, 700)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        
        #Aplica bordas arredondadas ao widget
        self.setStyleSheet("QWidget { border-radius: 10px; background-color: #DCDCDC; }")


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.setBackground(QColor(220, 220, 220))  # Define uma cor cinza claro como fundo
        painter.setBackgroundMode(Qt.OpaqueMode)  # Define o modo de fundo para opaco
        painter.eraseRect(event.rect())
        
        

        # Desenha a curva de Bézier
        painter.setPen(QPen(Qt.red, 4))
        bezier_points = self.calculate_bezier_points()
        painter.drawPolyline(QPolygonF(bezier_points))

          # Desenha o objeto animado
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#006400"))  # Verde escuro
        current_point = bezier_points[self.current_point_index]
        painter.drawEllipse(current_point, 10, 10)  # Diâmetro do ponto = 10 pixels

        # Desenha os pontos de controle
        painter.setPen(QPen(Qt.blue, 8, Qt.SolidLine))
        for point in self.points:
            painter.drawRect(QRect(point.x() - 4, point.y() - 4, 8, 8))

    def calculate_bezier_points(self):
        # Calcula os pontos de interpolação da curva de Bézier
        bezier_points = []
        for t in range(101):
            t /= 100.0
            point = self.calculate_bezier_point(t)
            bezier_points.append(point)
        return bezier_points

    def calculate_bezier_point(self, t):
        # Calcula um ponto da curva de Bézier para um valor de parâmetro t
        n = self.num_points - 1
        result = QPoint(0, 0)
        for i, point in enumerate(self.points):
            binomial_coefficient = self.combination(n, i)
            result += binomial_coefficient * ((1 - t) ** (n - i)) * (t ** i) * point
        return result

    def combination(self, n, k):
        # Calcula o coeficiente binomial (n choose k)
        numerator = self.factorial(n)
        denominator = self.factorial(k) * self.factorial(n - k)
        return numerator // denominator

    def factorial(self, n):
        # Calcula o fatorial de um número
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result

    def mousePressEvent(self, event):
        # Verifica se o usuário clicou em algum ponto de controle
        for i, point in enumerate(self.points):
            if QRect(point.x() - 4, point.y() - 4, 12, 12).contains(event.pos()):
                self.selected_point = i
                break

    def mouseMoveEvent(self, event):
        if self.selected_point is not None:
            self.points[self.selected_point] = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        self.selected_point = None
        self.update()
    
    def update_animation(self):
        self.timer.start(100)
        # Atualiza a posição do objeto animado ao longo da curva de Bézier
        t = (self.current_point_index + 1) / 100  # Normaliza o índice para o intervalo de 0 a 1
        
        # Incrementa o índice e verifica se ele excede o tamanho da lista de pontos
        self.current_point_index += 1
        if self.current_point_index >= 100:
            self.current_point_index = 0
            
        self.update()





