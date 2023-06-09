#kept in a seperate file as the code for these scenes are huge
from manim import *
from math import sin, cos, radians

class RotationMatrix(Scene):
    def construct(self):
        size = 1

        v = Matrix([["x"], ["y"]]).scale(size)
        m = Matrix([[r"\cos(\theta)", r"\sin(\theta)"],
                    [r"-\sin(\theta)", r"\cos(\theta)"]],
                   h_buff=2 * LARGE_BUFF,
                   bracket_h_buff=SMALL_BUFF,
                   ).scale(size)
        v.next_to(m, LEFT, buff=0.5)
        sol = Matrix([[r"x\cos(\theta)+y\sin(\theta)"],
                      [r"-x\sin(\theta)+y\cos(\theta)"]],
                     h_buff=2 * LARGE_BUFF,
                     bracket_h_buff=SMALL_BUFF,
                     ).scale(size)

        eq = Tex("=", color=BLUE).scale(size)
        result_objects = VGroup(*sol)

        braces = result_objects[1:]
        eq.shift(RIGHT * 0.5)
        m.next_to(eq, LEFT)
        v.next_to(m, LEFT)
        sol.next_to(eq, RIGHT)
        self.play(Write(v))
        self.wait(5)
        self.play(Write(m), Write(eq))
        self.play(*(Write(brace) for brace in braces))
        self.wait()

        v_rect = SurroundingRectangle(v.get_columns()[0])
        self.play(FadeIn(v_rect))

        last_h_rect = None
        for entry, row in zip(sol.get_entries(), m.get_rows()):
            h_rect = SurroundingRectangle(m.get_rows()[0])
            if last_h_rect:
                h_rect = SurroundingRectangle(row)
                self.play(Transform(last_h_rect, h_rect))
                self.remove(h_rect)
                h_rect = last_h_rect
            else:
                self.play(FadeIn(h_rect))
            last_h_rect = h_rect
            v1 = v_rect.copy()
            h1 = h_rect.copy()
            self.play(Transform(v1, h1, run_time=1))
            self.play(Transform(h1, entry, run_time=1))
            self.add(entry)
            self.remove(h1)
            self.remove(v1)
        self.wait()
        self.play(FadeOut(VGroup(v,m,eq,v_rect,last_h_rect)))
        self.play(sol.animate.move_to(ORIGIN))
        self.wait(2)
        self.play(Unwrite(braces))
        self.play(sol.animate.scale(1.5))
        self.wait(13)

class ExplainXAndY(Scene):
    def construct(self):
        scale = 2.5
        plane = NumberPlane().scale(scale).move_to(ORIGIN)
        radius = 1

        c = Circle(radius=radius).move_to(plane.c2p(0, 0)).scale(scale)
        self.play(Create(plane))
        theta = ValueTracker(radians(60))
        plane_origin = plane.c2p(0, 0)

        def get_x_and_y():
            return [
                cos(theta.get_value()) * radius,
                sin(theta.get_value()) * radius
            ]

        hyp = always_redraw(
            lambda: Line(plane_origin, plane.c2p(*get_x_and_y()))
        )
        base_x = always_redraw(
            lambda: Line(plane_origin, plane.c2p(get_x_and_y()[0], 0))
        )
        base_y = always_redraw(
            lambda: Line(plane.c2p(get_x_and_y()[0], 0), plane.c2p(*get_x_and_y()))
        )
        y_height = always_redraw(
            lambda: DashedLine(plane.c2p(0,get_x_and_y()[1]), plane.c2p(*get_x_and_y()))
        )

        def dot():
            d = Dot(plane.c2p(*get_x_and_y()))
            d.add(
                Tex("Joystick Position").scale(0.8).next_to(d,UR)
            )
            return d
        d = always_redraw(dot)

        arc = always_redraw(
            lambda: Angle.from_three_points(
                plane.c2p(get_x_and_y()[0]),
                plane_origin,
                plane.c2p(*get_x_and_y())) if theta.get_value()<radians(90) else
                Angle.from_three_points(
                    plane.c2p(*get_x_and_y()),
                    plane_origin,
                    plane.c2p(get_x_and_y()[0])
                )
        )
        show_func = ValueTracker(False)
        label = always_redraw(
            lambda: MathTex(r"\alpha").next_to(arc, UR+DOWN*0.75, buff=0.1) if theta.get_value()<radians(90) else
            MathTex(r"\alpha").next_to(arc, UL+DOWN*0.75, buff=0.1)
        )
        x_label = always_redraw(
            lambda: MathTex("x").next_to(base_y, DOWN) if not show_func.get_value() else MathTex(r"\cos(\alpha)").next_to(base_y, DOWN)
        )
        y_label = always_redraw(
            lambda: MathTex("y").next_to(y_height, LEFT) if not show_func.get_value() else MathTex(r"\sin(\alpha)").next_to(y_height,LEFT)
        )

        self.play(Create(c))
        self.play(Create(hyp), Create(base_x), Create(base_y), Create(arc), Create(label), Create(d))
        self.wait()
        self.play(Create(y_height), Create(x_label), Create(y_label))
        self.wait(2)
        self.play(theta.animate.set_value(radians(20)))
        self.wait()
        self.play(theta.animate.set_value(radians(75)))
        self.wait()
        self.play(theta.animate.set_value(radians(150)))
        self.wait()
        show_func.set_value(True)
        self.play(Transform(x_label,
                            MathTex(r"\cos(\alpha)").next_to(base_y, DOWN)),
                  Transform(y_label,
                            MathTex(r"\sin(\alpha)").next_to(y_height, LEFT)))
        self.play(theta.animate.set_value(radians(120)))
        self.wait()
        self.play(theta.animate.set_value(radians(45)))
        self.wait(3)

class FormulaMagic(Scene):
    def construct(self):
        orgCos = MathTex(r"x\cos(\theta)+y\sin(\theta)")
        orgSin = MathTex(r"y\cos(\theta)-x\sin(\theta)")
        subCos = MathTex(r"\cos(\alpha)\cos(\theta)+\sin(\alpha)\sin(\theta)")
        subSin = MathTex(r"\sin(\alpha)\cos(\theta)-\cos(\alpha)\sin(\theta)")
        fullCos = MathTex(r"\cos(\alpha-\theta)=\cos(\alpha)\cos(\theta)+\sin(\alpha)\sin(\theta)")
        fullSin = MathTex(r"\sin(\alpha-\theta)=\sin(\alpha)\cos(\theta)-\cos(\alpha)\sin(\theta)")
        eq = VGroup(orgCos,orgSin).arrange_in_grid(rows=2)
        VGroup(subCos, subSin).arrange_in_grid(rows=2)
        VGroup(fullCos, fullSin).arrange_in_grid(rows=2)
        self.play(Write(eq))
        self.wait()
        self.play(Transform(orgCos, subCos), Transform(orgSin, subSin))
        self.wait(2)
        self.play(Transform(orgCos, fullCos), Transform(orgSin, fullSin))
        self.wait(3)

class RobotLinearTransformationPi(LinearTransformationScene):


    def __init__(self, theta=radians(90)):
        super().__init__()
        LinearTransformationScene.__init__(self,leave_ghost_vectors=True)
        self.radians = theta

    def construct(self):
        self.radians = self.radians if self.radians else radians(90)
        c2p = self.background_plane.c2p
        robot = Square().rotate(self.radians, about_point=c2p(0,0))
        robot_vec = Vector([0, 2], color=PINK).rotate(self.radians, about_point=c2p(0,0))
        self.add(robot)
        self.add_vector(robot_vec)
        mat = np.array([
            [np.cos(self.radians), np.sin(self.radians)],
            [-np.sin(self.radians), np.cos(self.radians)]
        ])
        self.wait(4)
        self.moving_mobjects = []
        self.apply_matrix(mat)
        self.moving_mobjects = []
        self.wait(7)
        self.moving_mobjects = []
        self.apply_inverse(mat)
        self.moving_mobjects = []
        self.wait(3)

class RobotLinearTransformationOther(RobotLinearTransformationPi):
    def __init__(self):
        super().__init__(radians(-120))