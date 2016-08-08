import os
import glob
import json
import time
from collections import OrderedDict

from sample_data import sample_nodes, sample_links

click_default = '''function click(d) {
  if (d3.event.defaultPrevented) return;
  console.log('clicked');
}
'''

def rst(s, *repls): 
    '''Really stupid templates
       Yeah, so templates might be better. Meh.'''
    for name, value in repls:
        s = s.replace('${'+name+'}', str(value))
    return s

def rst_file(filename, *repls):
    with open(filename) as fid:
        s = fid.read()
    return rst(s, *repls)

def render_d3_fdg(dat, scale=1, force_scale=1, canvas_wh=(800, 800), save_freq='null',
                  click_function=click_default, js_filename='fdg.html.template'):
    f = '/tmp/index.html'
    w, h = canvas_wh
    s = rst_file(js_filename,
                 ('scale', scale),
                 ('force_scale', force_scale),
                 ('canvasw', w),
                 ('canvash', h),
                 ('save_freq', save_freq),
                 ('click_function', click_function),
                 ('graph', json.dumps(dat)),
    )
    with open(f, 'w') as fid:
        fid.write(s)
    
    os.system('xdg-open '+f)

def fdg(nodes, links, **kwds):
    d = OrderedDict([
        ("nodes", [OrderedDict([("id", _id), ("group", group)])
                  for _id, group in nodes]),
        ("links", [OrderedDict([("source", source), ("target", target), ("value", value)])
                  for source, target, value in links]),
    ])
    return render_d3_fdg(d, **kwds)

def do_cmd(cmd):
    print cmd
    return os.system(cmd)

def file_stem(filename):
    return os.path.splitext(os.path.split(filename)[-1])[0]

def string_between(s, before, after):
    return s.split(before)[1].split(after)[0]

def _generate_pngs(svg_base, dout, out_base, png_wh):
    w, h = png_wh
    for fin in glob.glob(svg_base):
        f = file_stem(fin)
        f = 'newesttree (0)' if f == 'newesttree' else f # For consistency
        i = int(string_between(f, '(', ')'))
        fout = os.path.join(dout, '{}_{:03d}.png'.format(out_base, i))
        do_cmd('inkscape -z -e "{fout}" -w {w} -h {h} "{fin}" -y=1'
               .format(fin=fin, fout=fout, w=w, h=h))

def _generate_gif(dout, out_base, animation_delay=20, display=True):
    pngs = os.path.join(dout, out_base+ '_*.png')
    gif = os.path.join(dout, 'animation.gif')
    do_cmd('convert -delay {delay} -loop 0 {pngs} {gif}'.format(delay=animation_delay,
                                                                pngs=pngs, gif=gif))
    if display:
        do_cmd('eog {}'.format(gif))

def _handle_save_freq_options(save_freq, total_steps=300):
    '''Handle multiple string options for save_freq (see docs for fdg_plus_images)
       total_steps is the number of time steps d3 seems to takes in the sim (always 300?)
       Returns:
       save_freq: JS-friendly format (integer or 'null')
       ignore_first: boolean flag that controls which svgs get processed to images'''
    ignore_first = (save_freq == 'last')
    sf_dict = {None: 'null',
               'first_last': total_steps-1,
               'last': total_steps-1,
               'first': 10000000,
               'all': 1,
               -1: total_steps-1, # ??
              }
    save_freq = sf_dict[save_freq] if save_freq in sf_dict else save_freq
    return save_freq, ignore_first

def fdg_plus_images(nodes, links,
                    save_freq='last',
                    png_wh=(1200, 1200),
                    sleep_time=10,
                    out_base='out',
                    dout='/tmp/',
                    clean_downloads=True,
                    clean_tmp=True,
                    animate=True,
                    animation_delay=20,
                    display=True,
                    **kwds
                   ):
    '''Render a D3 graph, save svg's at various points, and then use
       inkscape and ImageMagick (convert) to create pngs and then an
       animated gif
       Input kwd args:
       save_freq: Control the number of svg's saved from the simulation
                  one of: None or 'null', 'last' (default), 'first', 'first_last', 'all'
                          or any integer
       png_wh: Canvas size of output pngs, default (1200, 1200)
       sleep_time: Time to wait before starting the png conversion, default 10s
       out_base: name of the output png files default 'out'
       dout: output directory, default '/tmp/'
       clean_downloads: When True (default), clear the Downloads folder of names like newesttree*.svg
       clean_tmp: When True (default), clear the output directory of names matching the output pattern
       animate: When True (default), create an animated gif from the generated pngs
       display: When True (default), open the gif with eog
       
       All other **kwds get passed to render_d3_fdg thru fdg'''
    svg_base = os.path.expanduser('~/Downloads/newesttree*.svg')
    save_freq, ignore_first = _handle_save_freq_options(save_freq)
    if clean_downloads:
        do_cmd('rm '+ svg_base)
    if clean_tmp:
        do_cmd('rm {}_*.png'.format(os.path.join(dout, out_base)))
    if ignore_first:
        svg_base = svg_base.replace('*', ' (*)')
    fdg(nodes, links, save_freq=save_freq, **kwds)
    
    if save_freq != 'null':
        time.sleep(sleep_time)
        _generate_pngs(svg_base, dout, out_base, png_wh)
        
        if animate:
            _generate_gif(dout, out_base, animation_delay=animation_delay, display=display)

if __name__ == '__main__':
    #fdg(sample_nodes, sample_links, save_freq=60) # version that auto-DL's svgs
    #fdg_plus_images(sample_nodes, sample_links, save_freq=20) # version that auto-DL's svg's AND converts to pngs and animated gif
    #fdg_plus_images(sample_nodes, sample_links) # saves just the image of the final render
    fdg_plus_images(sample_nodes, sample_links, save_freq=None, js_filename='fdg_with_slider.html.template') # disabled saving, best for testing
    
