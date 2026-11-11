#include "py/runtime.h"

static mp_obj_t hello_answer(void) {
    return MP_OBJ_NEW_QSTR(MP_QSTR_hello);
}
static MP_DEFINE_CONST_FUN_OBJ_0(hello_answer_obj, hello_answer);

static const mp_rom_map_elem_t hello_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_hello) },
    { MP_ROM_QSTR(MP_QSTR_answer), MP_ROM_PTR(&hello_answer_obj) },
};
static MP_DEFINE_CONST_DICT(hello_globals, hello_globals_table);

const mp_obj_module_t hello_user_cmodule = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&hello_globals,
};
MP_REGISTER_MODULE(MP_QSTR_hello, hello_user_cmodule);
