" Language:     Colored CSS Color Preview
" Author:       Max Vasiliev <vim@skammer.name>
" Modified By:  Eiichi Sato <sato.eiichi@gmail.com>
" Last Change:  2011 Jul 31
" Licence:      No Warranties. WTFPL. But please tell me!
" Version:      0.7.1

if !has("gui_running") && &t_Co != 256
	finish
endif

if !has('python') && !has('python3')
	echoerr 'vim-css-color: Python interface not available. See :help +python or +python3.'
	finish
endif

" HACK modify cssDefinition to add @cssColors to its contains
redir => s:olddef
silent! syn list cssDefinition
redir END
if s:olddef != ''
	let s:b = strridx(s:olddef, 'matchgroup')
	if s:b != -1
		exe 'syn region cssDefinition' strpart(s:olddef, s:b).',@cssColors'
	endif
endif

call csscolor#define_named_colors()

for i in range(1, line('$'))
	call csscolor#colorize_line(i)
endfor

augroup csscolor
	autocmd!
	autocmd CursorMoved * silent call csscolor#colorize_line('.')
	autocmd CursorMovedI * silent call csscolor#colorize_line('.')
augroup END

