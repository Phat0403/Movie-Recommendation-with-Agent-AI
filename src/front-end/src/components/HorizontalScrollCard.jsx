import React from 'react'
import Card from './Card';
import { FaAngleLeft, FaAngleRight } from 'react-icons/fa6';
import { useRef } from 'react';

const HorizontalScrollCard = ({data = [], heading}) => {

    const containerRef = useRef();
    const handleNext = () => {
        containerRef.current.scrollLeft +=300
    }
    const handlePrevious = ()=>{
        containerRef.current.scrollLeft -=300
    }
  return (
    <div className="container mx-auto px-3 my-10">
        <h2 className="text-xl lg:text-2xl text-white font-bold mb-3">
          {heading}
        </h2>
        <div className="relative">
          <div ref={containerRef} className="grid grid-cols-[repeat(auto-fit,260px)] gap-6 grid-flow-col overflow-x-scroll overflow-hidden z-10 relative scroll-smooth transition-all scrollbar-none">
            {data.map((data, index) => {
              return (
                <Card
                  data={data}
                  key={data.tconst+heading+index}
                  index={index + 1}
                  trending={true}
                />
              );
            })}
          </div>
          <div className='absolute top-0 hidden lg:flex justify-between items-center w-full h-full '>
            <button onClick={handlePrevious} className=" bg-white p-1 rounded-full text-xl -ml-2 z-20 text-black cursor-pointer">
              <FaAngleLeft />
            </button>
            <button onClick={handleNext} className=" bg-white p-1 rounded-full text-xl -mr-2 z-10 text-black cursor-pointer">
              <FaAngleRight />
            </button>
          </div>
        </div>
      </div>
  )
}

export default HorizontalScrollCard