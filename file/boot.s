.section .bss
.align 16
stack_bottom:
.skip 16384 # 16 KiB
stack_top:



.global _starts

.global screens
.global fpc_do_exit			
.global FPC_LIB_EXIT
.global PC_LIB_EXIT
.global fpc_initializeunits
.global fpc_libinitializeunits
.global THREADVARLIST_$SYSTEM$indirect
.global INIT$_$SYSTEM
.extern main
.section .text
_starts:
	
	call main
FPC_LIB_EXIT:
	ret
haltss:
    jmp haltss
    INIT$_$SYSTEM:
screens:
THREADVARLIST_$SYSTEM$indirect:

PC_LIB_EXIT:
fpc_do_exit:
fpc_initializeunits:
ret