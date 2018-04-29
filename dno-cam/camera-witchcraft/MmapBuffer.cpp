/*
 * MmapBuffer.cpp
 *
 *  Created on: 29 апр. 2018 г.
 *      Author: snork
 */

#include "MmapBuffer.hpp"

#include <sys/mman.h>
#include <errno.h>

#include <system_error>

#include "../common/log.hpp"

namespace Cam
{

	MmapBuffer::MmapBuffer():
		::Logable<MmapBuffer>("MapBuffer")
	{}

	MmapBuffer::~MmapBuffer () {
		try {
			unmap();
		} catch (std::exception & e) {
			LOG_ERROR << "Ошибка в деструкторе MmapBuffer: \"" << e.what() << "\"" << std::endl;
		}
	}


	MmapBuffer::MmapBuffer(MmapBuffer && other)
		: Logable<MmapBuffer>("MapBuffer"), _ptr(other._ptr), _len(other._len), _index(other._index)
	{
		other._ptr = nullptr;
		other._len = 0;
		other._index = -1;
	}


	MmapBuffer & MmapBuffer::operator=(MmapBuffer && other)
	{
		_ptr = std::move(other._ptr);
		_len = std::move(other._len);
		_index = std::move(other._index);

		other._ptr = nullptr;
		other._len = 0;
		other._index = -1;

		return *this;
	}


	void MmapBuffer::map(int fd, int index, offset_t offset, length_t len)
	{
		unmap();

		_ptr = mmap(NULL /* start anywhere */,
			len,
			PROT_READ | PROT_WRITE /* required */,
			MAP_SHARED /* recommended */,
			fd, offset
		);

		if (MAP_FAILED == _ptr)
			throw std::system_error(errno, std::system_category(), " MMAP_FAILED");

		_len = len;
		_index = index;
	}


	void MmapBuffer::unmap()
	{
		if (!_ptr)
			return;

		if (0 > munmap(_ptr, _len))
			throw std::system_error(errno, std::system_category(), "не могу выполнить munamap!");

		_ptr = nullptr;
		_len = 0;
		_index = -1;
	}


	void swap(MmapBuffer & left, MmapBuffer & right)
	{
		std::swap(left._ptr, right._ptr);
		std::swap(left._len, right._len);
	}

}
