from typing import Tuple, Optional
import gradio

import ultraface.globals
from ultraface import wording
from ultraface.face_store import clear_static_faces, clear_reference_faces
from ultraface.uis.typing import File
from ultraface.filesystem import is_image, is_video
from ultraface.uis.core import register_ui_component

TARGET_FILE : Optional[gradio.File] = None
TARGET_IMAGE : Optional[gradio.Image] = None
TARGET_VIDEO : Optional[gradio.Video] = None


def render() -> None:
	global TARGET_FILE
	global TARGET_IMAGE
	global TARGET_VIDEO

	is_target_image = is_image(ultraface.globals.target_path)
	is_target_video = is_video(ultraface.globals.target_path)
	TARGET_FILE = gradio.File(
		label = wording.get('uis.target_file'),
		file_count = 'single',
		file_types =
		[
			'.png',
			'.jpg',
			'.webp',
			'.mp4'
		],
		value = ultraface.globals.target_path if is_target_image or is_target_video else None
	)
	TARGET_IMAGE = gradio.Image(
		value = TARGET_FILE.value['name'] if is_target_image else None,
		visible = is_target_image,
		show_label = False
	)
	TARGET_VIDEO = gradio.Video(
		value = TARGET_FILE.value['name'] if is_target_video else None,
		visible = is_target_video,
		show_label = False
	)
	register_ui_component('target_image', TARGET_IMAGE)
	register_ui_component('target_video', TARGET_VIDEO)


def listen() -> None:
	TARGET_FILE.change(update, inputs = TARGET_FILE, outputs = [ TARGET_IMAGE, TARGET_VIDEO ])


def update(file : File) -> Tuple[gradio.Image, gradio.Video]:
	clear_reference_faces()
	clear_static_faces()
	if file and is_image(file.name):
		ultraface.globals.target_path = file.name
		return gradio.Image(value = file.name, visible = True), gradio.Video(value = None, visible = False)
	if file and is_video(file.name):
		ultraface.globals.target_path = file.name
		return gradio.Image(value = None, visible = False), gradio.Video(value = file.name, visible = True)
	ultraface.globals.target_path = None
	return gradio.Image(value = None, visible = False), gradio.Video(value = None, visible = False)
