"""
技能模块

包含基于 czsc 库的各种量化交易技能
"""

from czsc_skills.skills.bi_recognition import BiRecognitionSkill
from czsc_skills.skills.signal_generator import SignalGeneratorSkill
from czsc_skills.skills.fractal_detector import FractalDetectorSkill

__all__ = [
    "BiRecognitionSkill",
    "SignalGeneratorSkill", 
    "FractalDetectorSkill",
]
