import React from 'react';
import { Nav, Navbar } from 'react-bootstrap';
import { Link, NavLink } from 'react-router-dom';

const NavBar = () => {
  return (
    <Navbar bg="dark" variant="dark">
      <Navbar.Brand as={Link} href='/' to='/'>Cloud Tracking</Navbar.Brand>
      <Nav className="ml-auto">
        <Nav.Link as={NavLink} href='/' to='/' exact>HOME</Nav.Link>
        <Nav.Link as={NavLink} href='/archive' to='/archive'>ARCHIVE</Nav.Link>
      </Nav>
    </Navbar>
  );
}

export default NavBar;