import type { DefaultTheme } from 'vitepress/types'


export default {
    sidebar: {
        '/referencia/': [
            {
                text: 'Componentes',
                link: '/referencia/componentes/',
                collapsed: false,
                items: [
                    {
                        text: 'Estágios',
                        collapsed: true,
                        items: [
                            {
                                text: 'IF - Busca Instrução',
                                link: '/referencia/componentes/stage_if',
                            }, {
                                text: 'ID - Decodifica Instrução',
                                link: '/referencia/componentes/stage_id',
                            }, {
                                text: 'EX - Executa',
                                link: '/referencia/componentes/stage_ex',
                            }, {
                                text: 'MEM - Acessa à Memória',
                                link: '/referencia/componentes/stage_mem',
                            }, {
                                text: 'WB - Escreve o Retorno',
                                link: '/referencia/componentes/stage_wb',
                            },
                        ],
                    },  {
                        text: 'Módulos',
                        collapsed: true,
                        items: [
                            {
                                text: 'Arquivo de Registradores',
                                link: '/referencia/componentes/module_register_file',
                            },{
                                text: 'Contador de Programa',
                                link: '/referencia/componentes/module_program_counter',
                            }, {
                                text: 'Escrita de Retorno',
                                link: '/referencia/componentes/module_write_back',
                            }, {
                                text: 'Unidade de Controle',
                                link: '/referencia/componentes/module_control_unit',
                            }, {
                                text: 'Unidade de Execução',
                                link: '/referencia/componentes/module_execution_unit',
                            }, {
                                text: 'Unidade de Controle de execução',
                                link: '/referencia/componentes/module_execution_control_unit',
                            },
                        ],
                    }, {
                        text: 'RV32I',
                        collapsed: true,
                        items: [
                            {
                                text: 'Decodificador de instruções',
                                link: '/referencia/componentes/rv32i_instruction_decoder',
                            }, {
                                text: 'Arquivo de Registradores',
                                link: '/referencia/componentes/rv32i_register_file',
                            }, {
                                text: 'Bit da ULA',
                                link: '/referencia/componentes/rv32i_alu_bit',
                            }, {
                                text: 'ULA',
                                link: '/referencia/componentes/rv32i_alu',
                            }, {
                                text: 'Controlador da ULA',
                                link: '/referencia/componentes/rv32i_alu_controller',
                            },
                        ],
                    }, {
                        text: 'Genéricos',
                        collapsed: true,
                        items: [
                            {
                                text: 'Somador',
                                link: '/referencia/componentes/generic_adder',
                            }, {
                                text: 'Multiplexador 2x1',
                                link: '/referencia/componentes/generic_mux_2x1',
                            }, {
                                text: 'Multiplexador 4x1',
                                link: '/referencia/componentes/generic_mux_4x1',
                            }, {
                                text: 'RAM',
                                link: '/referencia/componentes/generic_ram',
                            }, {
                                text: 'ROM',
                                link: '/referencia/componentes/generic_rom',
                            }, {
                                text: 'Registrador',
                                link: '/referencia/componentes/generic_register',
                            }, //{
                            //    text: 'Extensor de sinal',
                            //    link: '/referencia/componentes/generic_signal_extender',
                            //}, {
                            //    text: 'Flip Flop',
                            //    link: '/referencia/componentes/generic_flip_flop',
                            //}, {
                            //    text: 'Debounce',
                            //    link: '/referencia/componentes/generic_debounce',
                            //}, {
                            //    text: 'Detector de borda',
                            //    link: '/referencia/componentes/generic_edge_detector',
                            //}, {
                            //    text: 'Contador',
                            //    link: '/referencia/componentes/generic_counter',
                            //},
                        ],
                    },
                ],
            }, {
                text: 'Instruções',
                link: '/referencia/isa/',
            }, {
                text: 'Pseudo-instruções',
                link: '/referencia/isa/pseudo',
            },
        ],
    },
} satisfies DefaultTheme.Config
