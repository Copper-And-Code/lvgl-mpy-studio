import json
from lvgl_mpy_studio.core.model import Project


def project_with(props, widget_type="button"):
    project = Project()
    project.set_display_size(1000, 500)
    project.add_widget(project.pages[0], widget_type, props, "w")
    return project, project.widgets[0]


def test_each_axis_scales_on_its_own():
    project, widget = project_with({"x": 100, "y": 50, "width": 200, "height": 100})
    project.scale_to(500, 500)
    assert (widget.props["x"], widget.props["y"], widget.props["width"], widget.props["height"]) == (50, 50, 100, 100)
    assert (project.display.width, project.display.height) == (500, 500)
    assert project.pages[0].canvasSize == (500, 500)


def test_scaled_project_stays_inside_the_screen():
    project, widget = project_with({"x": 900, "y": 400, "width": 100, "height": 100})
    project.scale_to(240, 240)
    assert not project.widgets_outside(240, 240)


def test_font_snaps_to_an_available_size():
    project, widget = project_with({"fontSize": 32})
    project.scale_to(500, 250)
    assert widget.props["fontSize"] == 16


def test_small_sizes_never_vanish():
    project, widget = project_with({"width": 2, "height": 1, "radius": 1})
    project.scale_to(100, 50)
    assert (widget.props["width"], widget.props["height"], widget.props["radius"]) == (1, 1, 1)


def test_zero_radius_stays_zero():
    project, widget = project_with({"radius": 0})
    project.scale_to(100, 50)
    assert widget.props["radius"] == 0


def test_same_size_changes_nothing():
    project, widget = project_with({"x": 33, "fontSize": 15})
    before = dict(widget.props)
    project.scale_to(1000, 500)
    assert widget.props == before


def test_components_have_no_geometry():
    project, widget = project_with({}, "buzzer")
    project.scale_to(100, 50)
    assert widget.props == {}


def test_custom_styles_scale_too():
    project, widget = project_with({})
    widget.customStyles = {"pad_top": 20, "shadow_ofs_x": -10, "radius": 0, "text_font_size": 32, "bg_opa": 200, "bg_color": "#112233"}
    project.scale_to(500, 250)
    assert widget.customStyles == {"pad_top": 10, "shadow_ofs_x": -5, "radius": 0, "text_font_size": 16, "bg_opa": 200, "bg_color": "#112233"}


def test_keep_remembers_the_design_size_through_save(tmp_path):
    project = Project("pagine")
    project.set_display_size(480, 480)
    project.add_widget(project.pages[0], "panel", {"x": 0, "y": 0, "width": 480, "height": 480}, name="fondo")
    project.resize(240, 240, "keep")
    path = tmp_path / "progetto.json"
    project.save(path)
    loaded = Project.load(path)
    assert loaded.pages[0].designSize == (480, 480)
    loaded.resize(480, 480, "keep")
    assert loaded.pages[0].designSize is None


def test_adapt_grows_and_shrinks_without_deforming():
    for size in ((960, 480), (240, 480), (960, 960)):
        project = Project("forme")
        project.set_display_size(480, 480)
        project.add_widget(project.pages[0], "panel", {"x": 190, "y": 190, "width": 100, "height": 100}, name="quadro")
        project.scale_to(*size, keep_aspect=True)
        props = project.find_widget("quadro").props
        assert props["width"] == props["height"]
        assert abs(props["x"] + props["width"] / 2 - size[0] / 2) <= 1 and abs(props["y"] + props["height"] / 2 - size[1] / 2) <= 1


def test_adapt_moves_a_grid_as_one():
    project = Project("griglia")
    project.set_display_size(600, 600)
    for row in range(3):
        for column in range(3):
            project.add_widget(project.pages[0], "button", {"x": 150 + column * 104, "y": 40 + row * 104, "width": 96, "height": 96}, name=f"cella_{row}_{column}")
    project.scale_to(300, 600, keep_aspect=True)
    cells = [project.find_widget(f"cella_{row}_{column}").props for row in range(3) for column in range(3)]
    gaps = {cells[index + 1]["x"] - cells[index]["x"] for index in (0, 1, 3, 4)} | {cells[index + 3]["y"] - cells[index]["y"] for index in range(6)}
    assert gaps == {52}


def test_adapt_keeps_a_widget_on_the_one_below_it():
    project = Project("anello")
    project.set_display_size(480, 480)
    project.add_widget(project.pages[0], "panel", {"x": 130, "y": 36, "width": 220, "height": 220}, name="anello")
    project.add_widget(project.pages[0], "panel", {"x": 304, "y": 58, "width": 18, "height": 18}, name="satellite")
    project.scale_to(800, 480, keep_aspect=True)
    ring, dot = project.find_widget("anello").props, project.find_widget("satellite").props
    assert (dot["x"] - ring["x"], dot["y"] - ring["y"]) == (174, 22)


def test_a_second_change_starts_from_the_adapted_page():
    project = Project("due")
    project.set_display_size(480, 480)
    project.add_widget(project.pages[0], "panel", {"x": 190, "y": 190, "width": 100, "height": 100}, name="quadro")
    project.resize(240, 240, "keep")
    project.adapt_page(project.pages[0])
    project.resize(480, 480, "adapt")
    assert project.pages[0].designSize is None
    assert project.find_widget("quadro").props["width"] == 100
    project.resize(240, 240, "keep")
    project.resize(960, 960, "adapt")
    assert project.pages[0].designSize is None and project.find_widget("quadro").props["width"] == 200


def test_line_points_follow_their_box():
    project = Project("linee")
    project.set_display_size(400, 400)
    project.add_widget(project.pages[0], "line", {"x": 100, "y": 100, "width": 200, "height": 100, "points": "0,0 200,100"}, name="linea")
    project.scale_to(200, 200, keep_aspect=True)
    assert project.find_widget("linea").props["points"] == "0,0 100,50"


def test_design_size_also_loads_from_an_object(tmp_path):
    path = tmp_path / "oggetto.json"
    project = Project("oggetto")
    project.save(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    data["pages"][0]["designSize"] = {"width": 320, "height": 240}
    path.write_text(json.dumps(data), encoding="utf-8")
    assert Project.load(path).pages[0].designSize == (320, 240)


def test_equal_groups_in_different_containers_move_apart():
    project = Project("contenitori")
    project.set_display_size(600, 300)
    for side, left in (("a", 0), ("b", 300)):
        project.add_widget(project.pages[0], "panel", {"x": left, "y": 0, "width": 300, "height": 300}, name=f"pannello_{side}")
    for side in ("a", "b"):
        parent = project.find_widget(f"pannello_{side}")
        for index in range(2):
            child = project.add_widget(project.pages[0], "button", {"x": 100 + index * 55, "y": 120, "width": 50, "height": 50}, name=f"tasto_{side}_{index}")
            child.parentId = parent.id
    project.scale_to(1200, 600, keep_aspect=True)
    first, second = project.find_widget("tasto_a_0").props, project.find_widget("tasto_b_0").props
    assert first["x"] == second["x"] and first["y"] == second["y"]
