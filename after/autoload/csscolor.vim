" Language:     Colored CSS Color Preview
" Author:       Max Vasiliev <vim@skammer.name>
" Modified By:  Eiichi Sato <sato.eiichi@gmail.com>
" Last Change:  2011 Jul 31
" Licence:      No Warranties. WTFPL. But please tell me!
" Version:      0.7.1

let s:cpo_save = &cpo
set cpo&vim

function! csscolor#initialize()
	let pycode = globpath(&rtp, 'autoload/csscolor.py')
	if has('python')
		let s:pyfile = 'pyfile'
		let s:python = 'python'
	elseif has('python3')
		let s:pyfile = 'py3file'
		let s:python = 'python3'
	else
		echoerr 'Python interface is not available.'
		finish
	endif
	execute s:pyfile pycode
endfunction
call csscolor#initialize()

function! csscolor#percentage_to_code(r, g, b)
	execute s:python "VimCSSColor.percentage_to_code('".a:r."','".a:g."','".a:b."')"
endfunction

function! csscolor#add_highlight(group, color)
	execute s:python "VimCSSColor.add_highlight('".a:group."', '".a:color."')"
endfunction

function! csscolor#is_syntax_exist(pattern, group)
	redir => s:currentmatch
	silent! exe 'syn list' a:group
	redir END
	return s:currentmatch =~ '/'.escape(a:pattern, '\').'/'
endfunction

function! csscolor#add_syntax(color, type, pattern, group)
	exe 'syn' a:type a:group a:pattern 'contained'
	exe 'syn cluster cssColors add='.a:group
	call csscolor#add_highlight(a:group, a:color)
endfunction

function! csscolor#add_syntax_match(color, pattern)
	let group = substitute(a:color, '^#', 'cssColor', '')
	if !csscolor#is_syntax_exist(a:pattern, group)
		call csscolor#add_syntax(a:color, 'match', '/'.a:pattern.'/', group)
	endif
endfunction

function! csscolor#add_syntax_keyword(color, name)
	let group = substitute(a:color, '^#', 'cssColor', '')
	call csscolor#add_syntax(a:color, 'keyword', a:name, group)
endfunction

function! csscolor#define_named_colors()
	execute s:python "VimCSSColor.define_named_colors()"
endfunction

function! csscolor#colorize_line(where)
	let line = getline(a:where)

	" process color code
	let pattern = '#[0-9A-Fa-f]\{3,6\}\>'
	for i in range(1, 100) " at maximum
		let found = matchlist(line, pattern, 0, i)
		if len(found) == 0 | break | endif

		if found[0] =~ '#\x\{6}$'
			call csscolor#add_syntax_match(found[0], found[0].'\>')
		elseif found[0] =~ '#\x\{3}$'
			let color = substitute(found[0], '\(\x\)\(\x\)\(\x\)', '\1\1\2\2\3\3', '')
			call csscolor#add_syntax_match(color, found[0].'\>')
		endif
	endfor

	" process rgb()-style
	let pattern = 'rgb[a]\=(\(\d\{1,3}\s*%\=\),\s*\(\d\{1,3}\s*%\=\),\s*\(\d\{1,3}\s*%\=\).\{-})'
	for i in range(1, 100) " at maximum
		let found = matchlist(line, pattern, 0, i)
		if len(found) == 0 | break | endif

		let color = csscolor#percentage_to_code(found[1], found[2], found[3])
		call csscolor#add_syntax_match(color, found[0])
	endfor
endfunction

let &cpo = s:cpo_save
unlet s:cpo_save
