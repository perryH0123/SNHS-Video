import math
from math import cos, sin, radians
import numpy as np
from manim import *


class OpeningQuote(Scene):
    def construct(self):
        words = Tex(
            """``Life and trigonometry both are the same. \\\\
            They both have formulas to solve problems but\\\\where which formula is applied;\\\\
            that’s difficult to understand.''"""
        )
        words.to_edge(UP)
        for mob in words.submobjects[0][8:8+12]:
            mob.set_color(GREEN)
        author = Tex("-Anonymous", color=YELLOW)
        author.next_to(words, DOWN, buff = 0.5)
        self.play(FadeIn(words))
        self.wait(1)
        self.play(Write(author, run_time=4))
        self.wait()


class Intro(Scene):
    def construct(self):
        scalene = Polygon(2*UP, 2*LEFT, DOWN+RIGHT)
        a1 = Angle.from_three_points(DOWN+RIGHT, 2*LEFT, 2*UP)
        a2 = Angle.from_three_points(2*LEFT, 2*UP, DOWN+RIGHT)
        a3 = Angle.from_three_points(2*UP, DOWN+RIGHT, 2*LEFT)
        group = VGroup(scalene, a1, a2, a3).set_y(-0.25).scale(1.2)
        angles = VGroup(a1,a2,a3)
        self.play(GrowFromCenter(scalene))
        self.play(Create(angles))
        self.wait(1)
        transform = [[1,0.5],[0,1.5]]
        transform2 = [[1.3, 0.9], [0.4, 0.8]]

        self.play(ApplyMatrix(transform, group, run_time=1))
        self.wait(1)
        self.play(ApplyMatrix(transform2, group, run_time=1))

class Calculus(Scene):
    def construct(self):
        axes = (
            Axes(
                x_range=[0,10,1],
                x_length=9,
                y_range=[0,20,5],
                y_length=6,
                axis_config={"include_numbers":True, "include_tip": False}
            )
            .to_edge(DL)
            .set_color(GRAY)
        )
        axes_labels = axes.get_axis_labels(x_label="x",y_label="y")

        func = axes.plot(
            lambda t: 2*math.sin(t)+4, x_range=[0, 10], color=TEAL
        )
        x = ValueTracker(7)
        dx = ValueTracker(3)

        secant = always_redraw(
            lambda: axes.get_secant_slope_group(
                x=x.get_value(),
                graph=func,
                dx=dx.get_value(),
                dx_line_color=YELLOW,
                dy_line_color=ORANGE,
                dx_label="dx",
                dy_label="dy",
                secant_line_color=GREEN,
                secant_line_length=8
            )
        )
        dot1 = always_redraw(
            lambda: Dot()
            .scale(0.7)
            .move_to(axes.c2p(x.get_value(),func.underlying_function(x.get_value())))
        )
        dot2 = always_redraw(
            lambda: Dot()
            .scale(0.7)
            .move_to(axes.c2p(
                x.get_value() + dx.get_value(),
                func.underlying_function(x.get_value() + dx.get_value())
            )
            )
        )
        self.add(axes, axes_labels, func)
        self.play(Create(VGroup(dot1, dot2, secant)))
        self.play(dx.animate.set_value(0.001), run_time=8)
        self.wait(2)
        self.play(x.animate.set_value(1),run_time=5)
        self.wait()
        self.play(x.animate.set_value(7), run_time=5)


class Holonomic(Scene):
    def construct(self):
        car = Rectangle(width=2, height=3, color=RED).shift(LEFT*2)
        car_label = Tex("Your Car").next_to(car, DOWN)
        robot = Square(color=BLUE).shift(RIGHT*2)
        robot_label = Tex("Robot").next_to(robot, DOWN)
        car_direction = DoubleArrow(start=ORIGIN, end=UP*4, color=GREEN).shift(LEFT*2 + DOWN*2)
        robot_direction = Arrow(start=ORIGIN, end=UP*2.5, color=PINK).shift(RIGHT*2)
        self.play(AnimationGroup(Create(VGroup(car, robot), run_time=2)))
        self.play(Write(car_label), Write(robot_label))
        self.play(AnimationGroup(GrowArrow(car_direction), GrowArrow(robot_direction)))
        self.wait(1)
        self.play(Rotate(robot_direction, 2*PI, about_point=RIGHT*2),run_time=2)


class HolonomicProblem(Scene):
    def construct(self):
        robot = Square()
        robot_forwards = Arrow(ORIGIN, 2*LEFT, color=PINK)
        robot_label = Tex("Front of\\\\the robot").next_to(robot_forwards,LEFT,buff=0.5)
        forwards = Arrow(ORIGIN, 2*UP, color=YELLOW)
        self.play(GrowFromCenter(robot))
        self.play(GrowArrow(robot_forwards), GrowArrow(forwards), Write(robot_label))
        self.wait(2)

class ThreeThings(Scene):
    def construct(self):
        req = Tex(r"\textbf{Prior Knowledge}").to_edge(UP, buff=1)
        one = Tex("1. $x^2 + y^2 \leq 1$").shift(UP).to_edge(LEFT).arrange(DOWN, center=False, aligned_edge=LEFT)
        two = Tex("2. Robot will always know it's direction through IMU").next_to(one,DOWN).to_edge(LEFT).arrange(DOWN, center=False, aligned_edge=LEFT)
        three = Tex("3. Robot is holonomic (unlimited movement in x and y)").next_to(two,DOWN).to_edge(LEFT).arrange(DOWN, center=False, aligned_edge=LEFT)
        self.play(Write(req))
        self.play(Write(one))
        self.play(Write(two))
        self.play(Write(three))

class RobotAndFieldCentric(Scene):
    def construct(self):
        robot = Square()
        robot_forwards = Arrow(ORIGIN, 2*LEFT, color=PINK)
        robot_label = Tex("Front of\\\\the robot").next_to(robot_forwards,LEFT,buff=0.5)
        forwards = Arrow(ORIGIN, 2*UP, color=YELLOW)
        title = Tex("Robot Centric")
        title.to_edge(UP)
        self.add(robot, robot_forwards, robot_label, title)
        self.wait(2)
        self.play(Indicate(robot_forwards))
        self.play(Transform(title,Tex("Field Centric").to_edge(UP)))
        self.wait(2)
        self.play(FadeOut(robot_forwards), FadeIn(forwards))
        self.wait(2)
        self.play(Indicate(forwards))


class DeltaArmDemo(Scene):
    def construct(self):
        pos = ValueTracker(3)
        a = always_redraw(
            lambda: DashedLine(LEFT, pos.get_value()*RIGHT, color=RED)
        )
        b = always_redraw(
            lambda: Line(LEFT, LEFT
                         + math.sqrt(20-(1+pos.get_value())**2)*UP,
                         color=BLUE)
        )
        c = always_redraw(
            lambda: Line(LEFT+math.sqrt(20-(1+pos.get_value())**2)*UP,
                         pos.get_value()*RIGHT, color=GREEN)
        )
        a_label, b_label, c_label = (
            always_redraw(lambda: MathTex("a", color=RED).next_to(a, DOWN)),
            always_redraw(lambda: MathTex("b", color=BLUE).next_to(b, LEFT)),
            always_redraw(lambda: MathTex("c", color=GREEN).next_to(c, UR, buff=-1))
        )

        h = Line(LEFT, LEFT+DOWN*3)
        h_label = MathTex("h").next_to(h,LEFT)

        a1 = MathTex("a", color=RED)
        b1 = MathTex("b", color=BLUE)
        c1 = MathTex("c", color=GREEN)
        plus, sq, eq = MathTex("+"), MathTex(r"^2").scale(0.8), MathTex("=")
        b1.shift(1.25*DOWN)
        plus.next_to(b1, LEFT)
        sq1 = sq.copy().next_to(plus, LEFT)
        a1.next_to(sq1,LEFT, buff=SMALL_BUFF)
        sq2 = sq.copy().next_to(b1, RIGHT, buff=SMALL_BUFF)
        eq.next_to(sq2, RIGHT)
        c1.next_to(eq, RIGHT)
        sq3 = sq.copy().next_to(c1, RIGHT, buff=SMALL_BUFF)
        exp = VGroup(sq1,sq2,sq3).shift(UP*0.2)
        given = Tex("c is held constant").next_to(b1,DOWN)
        given.submobjects[0][0].set_color(GREEN)
        new_math = MathTex(r"b=\sqrt{c^2-a^2}").next_to(given, DOWN)
        originalEq = VGroup(a1,b1,c1,plus,exp,eq)

        content = new_math.submobjects[0]
        content[0].set_color(BLUE)
        content[4].set_color(GREEN)
        content[7].set_color(RED)
        a0, b0, c0 = a_label.copy(), b_label.copy(), c_label.copy()
        oe0 = originalEq.copy()
        intermediates = VGroup(a0,b0,c0,oe0)

        p = always_redraw(lambda: Dot(pos.get_value()*RIGHT)) #point where a and c intersect
        self.play(Create(a),Create(b),Create(c))
        self.play(Write(a_label), Write(b_label), Write(c_label))
        self.play(Create(p))
        self.wait()
        self.play(pos.animate.set_value(2))
        self.wait()
        self.play(pos.animate.set_value(3.2))
        self.play(
            Write(exp),
            Write(plus),
            Write(eq)
        )
        self.play(Transform(a0, a1))
        self.play(Transform(b0, b1))
        self.play(Transform(c0, c1))
        self.play(Write(given))
        self.play(Transform(oe0,new_math))
        self.wait()
        self.play(Unwrite(VGroup(given, new_math, originalEq, intermediates)))
        self.play(Create(h))
        self.play(Write(h_label))
        self.wait(3)

class DeltaSystemOfEquations(Scene):
    def construct(self):
        radius = 3
        c = Circle(radius=radius, color=WHITE)
        x = ValueTracker(0)
        y = ValueTracker(0)

        arm1 = always_redraw(
            lambda: DashedLine(RIGHT*cos(radians(90))*radius+UP*sin(radians(90))*radius,
                               x.get_value() * RIGHT + y.get_value() * UP,
                               color=RED)
        )
        arm2 = always_redraw(
            lambda: DashedLine(RIGHT*cos(radians(210))*radius+UP*sin(radians(210))*radius,
                               x.get_value() * RIGHT + y.get_value() * UP,
                               color=RED)
        )
        arm3 = always_redraw(
            lambda: DashedLine(RIGHT * cos(radians(330)) * radius + UP*sin(radians(330)) * radius,
                               x.get_value() * RIGHT + y.get_value() * UP,
                               color=RED)
        )
        d = always_redraw(
            lambda: Dot(RIGHT*x.get_value()+UP*y.get_value(), color=WHITE)
        )

        self.play(Create(c), Create(arm1), Create(arm2), Create(arm3))
        self.play(Create(d))
        self.wait()
        self.play(x.animate.set_value(1.5), y.animate.set_value(1.5), run_time=2)
        self.wait()
        self.play(x.animate.set_value(-0.3), y.animate.set_value(-1), run_time=1)
        self.wait()
        self.play(x.animate.set_value(-1), y.animate.set_value(0))
        self.play(x.animate.set_value(0), y.animate.set_value(1))
        self.wait()

class LawOfCosines(Scene):
    def construct(self):
        radius = 2
        earth = Circle(radius, color=BLUE_D)
        satellite_pos = 0.5*RIGHT+3*UP
        receiver_pos = sin(radians(30))*UP*radius+cos(radians(30))*RIGHT*radius
        satellite = Dot(satellite_pos)
        earth_center = Dot(ORIGIN)
        receiver = Dot(receiver_pos, color="#fc2c03")
        Rs = Line(ORIGIN, satellite_pos, color=GREEN)
        Rs.add(MathTex("R_s").next_to(Rs,LEFT, buff=-0.1))
        Re = Line(ORIGIN, receiver_pos, color=RED)
        Re.add(MathTex("R_e").next_to(Re,DR, buff=-0.5))
        d = Line(receiver_pos,satellite_pos, color=BLUE)
        d.add(MathTex("d").next_to(d,RIGHT, buff=-0.2))
        arc = Angle.from_three_points(satellite_pos, ORIGIN, receiver_pos, other_angle=True)
        arc_label = arc.add(MathTex("L").next_to(arc, UR, buff=-0.01))
        visuals = VGroup(earth, satellite, receiver, earth_center)
        geometry = VGroup(Rs, Re, d, arc)

        self.play(Create(visuals))
        self.play(Create(geometry))
        self.wait()
        self.play(VGroup(visuals, geometry).animate.to_edge(LEFT))
        self.wait()

        eq1 = MathTex(r"d=\sqrt{R_e^2+R_s^2-2R_eR_s\cos(L)}").shift(RIGHT*2+UP*3)
        eq2 = MathTex(r"d^2=R_e^2+R_s^2-2R_eR_s\cos(L)").next_to(eq1,DOWN, buff=MED_LARGE_BUFF)
        eq3 = MathTex(r"d^2-R_e^2-R_s^2=-2R_eR_s\cos(L)").next_to(eq2,DOWN, buff=MED_LARGE_BUFF)
        eq4 = MathTex(r"\frac{R_e^2+R_s^2-d^2}{2R_eR_s}=\cos(L)").next_to(eq3,DOWN, buff=MED_LARGE_BUFF)
        eq5 = MathTex(r"L=\arccos(\frac{R_e^2+R_s^2-d^2}{2R_eR_s})").next_to(eq4,DOWN, buff=MED_LARGE_BUFF)

        self.play(Write(eq1))
        self.wait()
        self.play(Transform(eq1.copy(),eq2))
        self.wait()
        self.play(Transform(eq2.copy(), eq3))
        self.wait()
        self.play(Transform(eq3.copy(), eq4))
        self.wait()
        self.play(Transform(eq4.copy(), eq5))
        self.wait()

class ToF(Scene):
    def construct(self):
        sat = Square(0.5, color=GRAY).shift(LEFT*3)
        earth = Circle(1, color=BLUE).shift(RIGHT*3)
        l1 = Line(sat.get_center(), earth.get_center())
        msg = Dot(sat.get_center()).set_color(ORANGE)
        visuals = VGroup(msg, sat, earth, l1)
        eq1 = MathTex(r"d=\frac{1}{2}rt")
        eq2 = MathTex(r"d=\frac{1}{2}(300,000)t")
        self.play(Create(visuals))
        self.wait()
        self.add(msg)
        self.play(MoveAlongPath(msg, l1), rate_func=there_and_back_with_pause, run_time=4)
        self.wait()
        self.play(visuals.animate.to_edge(UP, LARGE_BUFF))
        self.play(Write(eq1))
        self.wait()
        self.play(Transform(eq1,eq2))


class SphereScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        s = Sphere(radius=1.8, color=BLUE, fill_opacity=0.8)
        self.play(Create(s), run_time=1)
        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(10)
        self.stop_ambient_camera_rotation()

class Outro(Scene):
    def construct(self):
        logo = ManimBanner().shift(UP)
        create_label = Tex(r"Created with Manim CE\\Source Code in Description").next_to(logo,DOWN)
        manim = VGroup(logo, create_label)
        copyright = Tex(r"\textcopyright Perry Han 2023").scale(0.5).to_edge(DOWN, MED_SMALL_BUFF)
        thank_you = Tex(r"Thank you to:")
        andy = Tex(r"Andy Born\\Chief Engineer, Technical Fellow (L1)\\Boeing").next_to(thank_you,DOWN)
        terry = Tex(r"Terry Domae\\Associate Director of System Engineering\\Raytheon Technologies").next_to(thank_you,DOWN)
        _3b1b = Tex(r"3b1b / Grant Sanderson\\for inspiration").next_to(thank_you, DOWN)
        self.play(Create(logo), Write(create_label))
        self.wait()
        self.play(manim.animate.scale(0.5))
        self.play(manim.animate.to_edge(UP), FadeIn(copyright))
        self.play(Write(thank_you), Write(andy))
        self.wait(3)
        self.play(Transform(andy, terry))
        self.wait(3)
        self.play(Transform(andy,_3b1b))
        self.wait(3)