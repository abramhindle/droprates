import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def ciPlot(rate,sub):
    fig,ax = plt.subplots(dpi=300, figsize=(6,4))
    ax.set_title("95%% Confidence Interval of %s percent droprate" % rate)
    ax.set_xlabel("Trials")
    ax.set_ylabel("Successes")
    ax.grid(which='Both')
    ax.step(sub[:,1],sub[:,3],label="High95CI",where="post",linewidth=2)
    ax.step(sub[:,1],sub[:,2],label="Low95CI",where="post",linewidth=1)
    ax.set_yscale('symlog')
    ax.set_xscale('symlog')
    ax.xaxis.set_major_locator(ticker.NullLocator())
    xticks = [1,2,4,7,10,20,30,50,100,200,500,1000]
    ax.set_xticks(xticks)#, [str(x) for x in ticks])
    xsf = ticker.ScalarFormatter()
    xsf.set_scientific(False)
    ax.xaxis.set_minor_formatter(xsf)
    ax.xaxis.set_major_formatter(xsf)
    yticks = [0,1,2,4,7,10,20,30,50,100,200,500]
    ax.set_yticks(yticks)#, [str(x) for x in ticks])
    #ax.yaxis.set_major_locator(ticker.NullLocator())
    ysf = ticker.ScalarFormatter()
    ysf.set_scientific(False)
    ax.yaxis.set_major_formatter(ysf)
    ax.yaxis.set_minor_formatter(ysf)
    ax.legend()
    return fig

def htmlTable(results):
    rates = sorted(list(set([x[0] for x in results])))
    ns = sorted(list(set([x[1] for x in results])))
    rows = []
    for n in ns:
        row = []
        row.append(str(n))
        sub = [x for x in results if x[1] == n]
        for rate in rates:
            s = [x for x in sub if x[0] == rate]
            rate,n,low,high = s[0]

            row.append(str(low))
            row.append(str(high))
        rows.append(row)
    out = []
    out.append('<table id="droprates">')
    out.append('<tr>')
    out.append('<th>Trials</th>')
    for rate in rates:
        out.append("<th>%s low</th><th>%s high</th>" % (rate,rate))
    for row in rows:
        out.append("<tr>")
        for col in row:
            out.append("<td>%s</td>" % col)
        out.append("</tr>")
    out.append('</table>')
    return "\n".join(out)                                

if __name__ == "__main__":
    with open('droprate.pickle', 'rb') as f:
        result = pickle.load(f)
        rates = sorted(list(set([x[0] for x in result])))
        ns = sorted(list(set([x[1] for x in result])))
        with open('droprate.html', 'w') as wf:
            wf.write(htmlTable(result))
        for rate in rates:
            sub = np.array([x for x in result if x[0] == rate])
            print(sub)
            fig = ciPlot(rate,sub)
            fig.savefig('ci95-droprate-{:08.4f}.pdf'.format(rate), bbox_inches='tight')
            fig.savefig('ci95-droprate-{:08.4f}.png'.format(rate), bbox_inches='tight')
            plt.close()
        
