+++
date = "2011-10-23T10:55:00-07:00"
draft = false
title = "Parallel Game of Life"
slug = "parallel-game-of-life"
tags = ["c++", "parallel"]

+++
Conway's <a href="http://www.bitstorm.org/gameoflife/">Game of Life</a> is a dramatic illustration of emmergent behavior; that a seemingly complex system, such as cell mitosis can be governed by a set of simple rules. OpenMP is a fantastic set of language extensions which allows one to add dramatic parallelism without complex thread management.  As a demonstration of <a href="http://openmp.org/wp/">OpenMP</a>'s simplicity I implemented the Game of Life. The code and all analysis is available on <a href="https://bitbucket.org/jwright/parallel-game-of-life">bitbucket.org</a>.

<!--more-->

In a real program, it common to have swathes of code which cannot be made parallel. OpenMP's limited perspective on data limits one further.  As such, OpenMP is most effective when the data is decomposed into independently manageable chunks. To evaluate the performance affect of OpenMP on my implementation I used a single Base Class to implement the serial portion of the code. Each child class makes small modifications to the generation calculation, decomposing the data in different ways.  I made three decompositions:
<ol>
	<li>Decomposition by Rows</li>
	<li>Decomposition by Columns</li>
	<li>Random Decomposition by Cell</li>
</ol>
<div>Interestingly, the relative performance of each mechanism was quite volatile. The serial version of the code is quite simple. Basically, calculate each live/die action for every cell then, after all calculations are made, commit the updates in one atomic action.</div>
<div>
<pre lang="cpp" escaped="true">void GameGrid::CalculateGeneration()
{
    list delayedUpdates;

    for(size_t col = 0; col &lt; GetGridSize(); ++col)
    {
        for(size_t row = 0; row &lt; GetGridSize(); ++row)
        {
            uint32_t livingNeighbors = CountLivingNeighbors(col, row);
#ifdef DEBUG
            cout &lt;&lt; "Row: " &lt;&lt; row
                &lt;&lt; "Col: " &lt;&lt; col
                &lt;&lt; ": " &lt;&lt; livingNeighbors &lt;&lt; endl;
#endif
            Update u;
            u.threadId = omp_get_thread_num();
            u.position = &amp;(Grid[col][row]);
            u.threadPosition = &amp;(GridThreads[col][row]);
            if(Grid[col][row]) //If Cell is alive
            {
                if(livingNeighbors = 4)
                {
                    //Kill Cell
                    u.updateValue = false;
                    delayedUpdates.push_back(u);
                }
                /* else remain alive */
            }
            else
            {
                if(livingNeighbors == 3)
                {
                    //ConceiveCell
                    u.updateValue = true;
                    delayedUpdates.push_back(u);
                }
            }

        }
    }
    commitUpdates(delayedUpdates);
}</pre>
</div>
Even this simple routine can generate incredible emergent behavior.

<video width="816" height="432" controls="controls"><source src="http://www.codestrokes.com/wp-content/uploads/2011/10/out-1.ogv" type="video/ogg" />
Your browser does not support the video tag.
</video>
<div>Now, we have a serial platform to extend into a parallel one. First we extend the base class with simple inheritance.</div>
<pre lang="cpp" escaped="true">class GameGridParallelCol : public GameGrid
{
    public:
        typedef std::tr1::shared_ptr Ptr; ///@note The Anderson Smart Pointer Idiom
        typedef std::tr1::weak_ptr WeakPtr;
        static GameGridParallelCol::Ptr construct(string filename, size_t size);
        virtual ~GameGridParallelCol();
        virtual void CalculateGeneration();
    protected:
    private:

        GameGridParallelCol(string filename, size_t size);
        GameGridParallelCol::WeakPtr self;

};</pre>
<div>The using OpenMP Directives add col decomposition:</div>
<pre lang="cpp" escaped="true">void GameGridParallelCol::CalculateGeneration()
{
    vector delayedUpdates[omp_get_max_threads()]; //Create duplicate update lists, to avoid critical sections.
   for(size_t row = 0; row &lt; GetGridSize(); ++row)
    {
#pragma omp parallel for
        for(size_t col = 0; col &lt; GetGridSize(); ++col)
        {
            uint32_t livingNeighbors = CountLivingNeighbors(col, row);</pre>
<div>

Here is the power of OpenMP, its simplicity.  OpenMP exposes a set of #pragma functions which apply parallelism to the beginning of a scope block, and a barrier at the end of the scope block. Automatic parallelism, it doesn't get easier than this. However OpenMP's simplicity does hamper it in a few ways. OpenMP directives for instance, cannot batch C++ iterators. Now we have a thread pool which will run segments of the game of life in parallel.

[caption id="attachment_420" align="aligncenter" width="792" caption="Column Order Decomposition"]<a href="http://www.codestrokes.com/wp-content/uploads/2011/10/Screenshot-at-2011-10-22-215034.png"><img class="size-full wp-image-420" title="Column Decomposition of Game of Life" src="http://www.codestrokes.com/wp-content/uploads/2011/10/Screenshot-at-2011-10-22-215034.png" alt="" width="792" height="396" /></a>[/caption]

The right half of the image illustrates each thread, one for each color, as it updates a section of the game grid.  (Decomposition into rows is left as an exercise). Extending this we can make a fully parallel version.

</div>
<pre lang="cpp" escaped="true">#pragma omp parallel for collapse(2) schedule(dynamic)
   for(size_t row = 0; row &lt; GetGridSize(); ++row)
    {
        for(size_t col = 0; col &lt; GetGridSize(); ++col)
        {
            uint32_t livingNeighbors = CountLivingNeighbors(col, row);</pre>
<div>

Rendering the following:

[caption id="attachment_422" align="aligncenter" width="792" caption="Full data decomposition with dynamic thread balancing"]<a href="http://www.codestrokes.com/wp-content/uploads/2011/10/CorrectedFullThreadRender.png"><img class="size-full wp-image-422" title="CorrectedFullThreadRender" src="http://www.codestrokes.com/wp-content/uploads/2011/10/CorrectedFullThreadRender.png" alt="" width="792" height="396" /></a>[/caption]

</div>
<div>Now we have a fully parallel version where threads calculate cells at random, as the thread is available. Strangely, this isn't always the fastest algorithm.</div>
<h2>Analysis</h2>
No single decomposition wins out. As such there is no generalization such that one threading mechanism is faster than another in all cases. The Full threading model was mst consistant, but the Row and Column decompositions actually got slower as more cores were added.

[caption id="attachment_423" align="aligncenter" width="695" caption="6-core Speedup"]<a href="http://www.codestrokes.com/wp-content/uploads/2011/10/fitted-speedup.png"><img class="size-large wp-image-423" title="6-corefitted-speedup" src="http://www.codestrokes.com/wp-content/uploads/2011/10/fitted-speedup-1024x768.png" alt="" width="695" height="521" /></a>[/caption]

[caption id="attachment_424" align="aligncenter" width="695" caption="12-core Speedup"]<a href="http://www.codestrokes.com/wp-content/uploads/2011/10/fitted-speedup1.png"><img class="size-large wp-image-424" title="12 corefitted-speedup" src="http://www.codestrokes.com/wp-content/uploads/2011/10/fitted-speedup1-1024x768.png" alt="" width="695" height="521" /></a>[/caption]

Most interestingly, the row and column performance goes down with more cores, while the full decomposition stays pretty constant. I do not have a reason why this is happening.
<h2>Conclusion</h2>
<div>OpenMP makes adding parallelism to a serial program easy. The constructs allow one to sprinkle parallel code throughout the program, and the measure the performance boost. Sometimes it may be prudent to dive in deeper and manually thread some section of code, especially when using complex C++ constructs such as iterators, but if OpenMP meets the need, then its a low-cost, cross-platform mechanism.  Furthermore, OpenMP is exposed as a set of #pragma functions. Since #pragmas are by definition an extension to the language, if the compiler doesn't understand the directives, they are simply ignored. This allows one to liberally use OpenMP, and if the compiler of choice doesn't support the OpenMP directives, OpenMP will not break the build. OpenMP is a fantastic tool.</div>
