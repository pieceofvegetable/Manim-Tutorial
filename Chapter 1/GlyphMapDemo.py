from manim import *

def ir(a,b): # inclusive range, useful for TransformByGlyphMap
    return list(range(a,b+1))


class TransformByGlyphMap(AnimationGroup):
    def __init__(self, mobA, mobB, *glyph_map, replace=True, from_copy=False, show_indices=False, **kwargs):
		# replace=False does not work properly
        if from_copy:
            self.mobA = mobA.copy()
            self.replace = True
        else:
            self.mobA = mobA
            self.replace = replace
        self.mobB = mobB
        self.glyph_map = glyph_map
        self.show_indices = show_indices

        animations = []
        mentioned_from_indices = []
        mentioned_to_indices = []
        for from_indices, to_indices in self.glyph_map:
            print(from_indices, to_indices)
            if len(from_indices) == 0 and len(to_indices) == 0:
                self.show_indices = True
                continue
            elif len(to_indices) == 0:
                animations.append(FadeOut(
                    VGroup(*[self.mobA[0][i] for i in from_indices]),
                    shift = self.mobB.get_center()-self.mobA.get_center()
                ))
            elif len(from_indices) == 0:
                animations.append(FadeIn(
                    VGroup(*[self.mobB[0][j] for j in to_indices]),
                    shift = self.mobB.get_center() - self.mobA.get_center()
                ))
            else:
                animations.append(Transform(
                    VGroup(*[self.mobA[0][i].copy() if i in mentioned_from_indices else self.mobA[0][i] for i in from_indices]),
                    VGroup(*[self.mobB[0][j] for j in to_indices]),
                    replace_mobject_with_target_in_scene=self.replace
                ))
            mentioned_from_indices.extend(from_indices)
            mentioned_to_indices.extend(to_indices)

        print(mentioned_from_indices, mentioned_to_indices)
        remaining_from_indices = list(set(range(len(self.mobA[0]))) - set(mentioned_from_indices))
        remaining_from_indices.sort()
        remaining_to_indices = list(set(range(len(self.mobB[0]))) - set(mentioned_to_indices))
        remaining_to_indices.sort()
        print(remaining_from_indices, remaining_to_indices)
        if len(remaining_from_indices) == len(remaining_to_indices) and not self.show_indices:
            for from_index, to_index in zip(remaining_from_indices, remaining_to_indices):
                animations.append(Transform(
                    self.mobA[0][from_index],
                    self.mobB[0][to_index],
                    replace_mobject_with_target_in_scene=self.replace
                ))
            super().__init__(*animations, **kwargs)
        else:
            print(f"From indices: {len(remaining_from_indices)}    To indices: {len(remaining_to_indices)}")
            print("Showing indices...")
            super().__init__(
                Create(index_labels(self.mobA[0], color=PINK)),
                FadeIn(self.mobB.next_to(self.mobA, DOWN), shift=DOWN),
                Create(index_labels(self.mobB[0], color=PINK)),
                Wait(5),
                lag_ratio=0.5
                )



class CisCube(Scene):
	def construct(self):
		expA = MathTex("\\left( \\cos(x) + i\\sin(x) \\right)^3")
		expB = MathTex("\\cos(3x) + i\\sin(3x)")
		self.add(expA)
		self.play(TransformByGlyphMap(expA,expB,
			([16], [4]),
			([16], [13]),
			([0,15], [])
		))



class MultiplyingBinomials(Scene):
    def construct(self):
        expA = MathTex("(x+3)(x+4)")
        expB = MathTex("x(x+4) + 3(x+4)")
        expC = MathTex("x^2 + 4x + 3x + 12")
        expD = MathTex("x^2 + 7x + 12")

        VGroup(expA, expB, expC, expD).arrange(DOWN)
        self.add(expA)
        self.play(
            TransformByGlyphMap(expA, expB,
                ([0,4],[]),
                ([1],[0]),
                ([2], [6]),
                ([3], [7]),
                ([5,6,7,8,9], [1,2,3,4,5]),
                ([5,6,7,8,9], [8,9,10,11,12]),
                from_copy=True
            )
        )
        self.wait()
        self.play(
            TransformByGlyphMap(expB, expC,
                ([1,5,8,12], []),
                ([0,2], [0,1]),
                ([0,4], [3,4]),
                ([7,9], [6,7]),
                ([7,11], [9,10]),
                from_copy=True
            )
        )
        self.wait()
        self.play(
            TransformByGlyphMap(expC, expD,
                ([3,4,5,6,7], [3,4]),
				from_copy=True
            )
        )



class QuadraticFormula(Scene):
	def construct(self):
		exps = [
            MathTex("ax^2 + bx + c = 0"),
            MathTex("ax^2 + bx = -c"),
            MathTex("x^2 + {b \\over a}x = - {c \\over a}"),
            MathTex("x^2 + {b \\over a}x + \\left({b \\over 2a}\\right)^2 = - {c \\over a} + \\left({b \\over 2a}\\right)^2"),
			MathTex("x^2 + {b \\over a}x + \\left({b \\over 2a}\\right)^2 = \\left({b \\over 2a}\\right)^2 - {c \\over a}"),
            MathTex("x^2 + {b \\over a}x + \\left({b \\over 2a}\\right)^2 = {b^2 \\over 4a^2} - {c \\over a}"),
            MathTex("x^2 + {b \\over a}x + \\left({b \\over 2a}\\right)^2 = {b^2 \\over 4a^2} - {4ac \\over 4a^2}"),
            MathTex("x^2 + {b \\over a}x + \\left({b \\over 2a}\\right)^2 = {b^2 - 4ac \\over 4a^2}"),
			MathTex("\\left( x + {b \\over 2a} \\right)^2 = {b^2 - 4ac \\over 4a^2}"),
            MathTex("x + {b \\over 2a} = \\pm \\sqrt{ {b^2 - 4ac \\over 4a^2} }"),
            MathTex("x + {b \\over 2a} = \\pm { \\sqrt{ b^2 - 4ac } \\over \\sqrt{ 4a^2 } }"),
            MathTex("x + {b \\over 2a} = \\pm { \\sqrt{ b^2 - 4ac } \\over 2a } }"),
			MathTex("x = - {b \\over 2a} \\pm { \\sqrt{ b^2 - 4ac } \\over 2a } }"),
            MathTex("x = { - b \\pm \\sqrt{ b^2 - 4ac } \\over 2a }"),
        ]
		for exp in exps:
			exp.scale(1.5)

		self.play(Write(exps[0]))
		self.wait()
		self.play(TransformByGlyphMap(exps[0], exps[1], # subtract c
			([6,7], [7,8]),
			([8], [6]),
			([9], [])
		))
		self.wait()
		self.play(TransformByGlyphMap(exps[1], exps[2], # divide by a
			([0], [5,11]),
			([], [4,10]),
		))
		self.wait()
		self.play(TransformByGlyphMap(exps[2], exps[3], # complete the square
			([], [*ir(7,14)]),
			([], [*ir(20,27)]),
		))
		self.wait()
		self.play(TransformByGlyphMap(exps[3], exps[4], # rhs reorder
			([*ir(21,27)], [*ir(16,22)]),
			([*ir(16,19)], [*ir(23,26)]),
			([20], [])
		))
		self.wait()
		self.play(TransformByGlyphMap(exps[4], exps[5], # rhs distribute square
			([22], [17]),
			([22], [21]),
			([22,19], [19]),
			([16,21], [])
		))
		self.wait()
		self.play(TransformByGlyphMap(exps[5], exps[6], # rhs common denominator
			([], [23,24,27,29]),
		))
		self.wait()
		self.play(TransformByGlyphMap(exps[6], exps[7], # rhs combine fractions
			([23,24,25], [19,20,21]),
			([22], [18]),
			([18], [22]),
			([26], [22]),
			([19,20,21], [23,24,25]),
			([27,28,29], [23,24,25])
		))
		self.wait()
		self.play(TransformByGlyphMap(exps[7], exps[8], # lhs rewrite
			([0,6], [1]),
			([2,7], [2]),
			([3,4,5], [3,4,6]),
			([9,10,11,12], [3,4,5,6]),
			([1,14], [8]),
			([8], [0]),
			([13], [7]),
		))
		self.wait()
		self.play(TransformByGlyphMap(exps[8], exps[9], # square root
			([8], [7,8,9]),
			([0,7], []),
		))
		self.wait()
		self.play(TransformByGlyphMap(exps[9], exps[10], # rhs distribute square root
			([8], [8,17]),
			([9], [9,18]),
		))
		self.wait()
		self.play(TransformByGlyphMap(exps[10], exps[11], # rhs simplify denominator
			([17,18], []),
			([19], [17]),
			([20,21], [18])
		))
		self.wait()
		self.play(TransformByGlyphMap(exps[11], exps[12], # final subtract
			([*ir(1,5)], [*ir(2,6)]),
		))
		self.wait()
		self.play(TransformByGlyphMap(exps[12], exps[13], # combine fractions
			([4], [13]),
			([16], [13]),
			([5,6], [14,15]),
			([17,18], [14,15])
		))
		self.wait()
		self.play(Circumscribe(exps[-1]))



class SumChange(Scene):
    def construct(self):
        tex1 = MathTex("\\sum_{k=1}^{9}")
        tex2 = MathTex("\\sum_{k=1}^{10}")

        self.play(Write(tex1, run_time=0.75))
        self.play(TransformByGlyphMap(tex1,tex2,
			([0], [0,1]),
			#show_indices=False
		))
        self.wait()

