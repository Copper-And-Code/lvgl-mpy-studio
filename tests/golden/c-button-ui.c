#include "ui.h"
#include "ui_events.h"

/* Fonts used: enable LV_FONT_MONTSERRAT_14 in lv_conf.h */

lv_obj_t * ui_button1;

static lv_obj_t * screens[1];
static int current_screen;

static void c_button_create_main(lv_obj_t * parent)
{
    if (parent == NULL) parent = lv_screen_active();
    /* button: button1 */
    ui_button1 = lv_button_create(parent);
    lv_obj_set_pos(ui_button1, 50, 50);
    lv_obj_set_size(ui_button1, 100, 40);
    lv_obj_set_style_bg_color(ui_button1, lv_color_hex(0x2196F3), LV_PART_MAIN);
    lv_obj_set_style_radius(ui_button1, 5, LV_PART_MAIN);
    lv_obj_t * button1_label = lv_label_create(ui_button1);
    LV_UNUSED(button1_label);
    lv_label_set_text(button1_label, "Button");
    lv_obj_center(button1_label);
    lv_obj_set_style_text_color(button1_label, lv_color_hex(0xFFFFFF), LV_PART_MAIN);
    lv_obj_set_style_text_font(button1_label, &lv_font_montserrat_14, LV_PART_MAIN);
}

void c_button_load_page(int page_index)
{
    if (page_index < 0 || page_index >= 1) return;
    if (screens[page_index] == NULL) {
        screens[page_index] = lv_obj_create(NULL);
        if (page_index == 0) {
            c_button_create_main(screens[page_index]);
        }
    }
    lv_screen_load(screens[page_index]);
    current_screen = page_index;
}

void ui_create(void)
{
    current_screen = 0;
    c_button_load_page(0);
}
