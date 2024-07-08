from typing import Optional
import gradio

import ultraface.globals
import ultraface.choices
from ultraface import wording

EXECUTION_THREAD_COUNT_SLIDER : Optional[gradio.Slider] = None


def render() -> None:
	global EXECUTION_THREAD_COUNT_SLIDER

	EXECUTION_THREAD_COUNT_SLIDER = gradio.Slider(
		label = wording.get('uis.execution_thread_count_slider'),
		value = ultraface.globals.execution_thread_count,
		step =ultraface.choices.execution_thread_count_range[1] - ultraface.choices.execution_thread_count_range[0],
		minimum = ultraface.choices.execution_thread_count_range[0],
		maximum = ultraface.choices.execution_thread_count_range[-1]
	)


def listen() -> None:
	EXECUTION_THREAD_COUNT_SLIDER.release(update_execution_thread_count, inputs = EXECUTION_THREAD_COUNT_SLIDER)


def update_execution_thread_count(execution_thread_count : int = 1) -> None:
	ultraface.globals.execution_thread_count = execution_thread_count

